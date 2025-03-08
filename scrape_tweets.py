from nite import Tweet
import json
import csv
from datetime import datetime
import time
import os

def save_tweets(writer, tweets, keyword):
    for tweet in tweets:
        writer.writerow([
            keyword,
            tweet['user']['username'],
            tweet['user']['name'],
            tweet['text'].replace('\n', ' '),
            tweet['date'],
            tweet['link'],
            tweet['stats']['comments'],
            tweet['stats']['retweets'],
            tweet['stats']['quotes'],
            tweet['stats']['likes'],
            ';'.join(tweet['media']['images']),
            ';'.join(tweet['media']['videos'])
        ])

def main():
    # Daftar kata kunci yang akan dicari
    kata_kunci = [
        # "indonesia gelap",
        # "anjing",
        # "bodoh",
        # "bangsat",
        # "bego",
        # "tolol",
        # "goblok",
        # "kontol",
        # "memek",
        "prabowo"
    ]
    
    # Nama file output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"tweets_kasar_{timestamp}.csv"
    
    # Membuat file CSV dan menulis header
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Keyword',
            'Username',
            'Name',
            'Tweet',
            'Date',
            'Link',
            'Comments',
            'Retweets',
            'Quotes',
            'Likes',
            'Images',
            'Videos'
        ])
        
        # Mencari tweet untuk setiap kata kunci
        for keyword in kata_kunci:
            print(f"\nMencari tweet dengan kata kunci: {keyword}")
            collected_tweets = 0
            max_retries = 3
            retry_count = 0
            
            while collected_tweets < 200 and retry_count < max_retries:
                try:
                    # Menghitung berapa tweet yang masih perlu diambil
                    remaining = 200 - collected_tweets
                    
                    hasil = Tweet.posts(
                        query=keyword,
                        limit=remaining,
                        since="2025-02-01",
                        until="2025-02-02",
                        lang="id",
                        verbose=True
                    )
                    
                    tweets = json.loads(hasil)
                    
                    if not tweets:  # Jika tidak ada tweet ditemukan
                        print(f"Tidak ada tweet ditemukan untuk '{keyword}' setelah {collected_tweets} tweet")
                        break
                    
                    # Menyimpan tweets ke CSV
                    save_tweets(writer, tweets, keyword)
                    
                    new_tweets = len(tweets)
                    collected_tweets += new_tweets
                    print(f"Berhasil mengambil {new_tweets} tweet baru. Total: {collected_tweets}/200")
                    
                    # Jika dapat tweet kurang dari yang diminta, mungkin sudah tidak ada lagi
                    if new_tweets < remaining:
                        print(f"Hanya menemukan {collected_tweets} tweet untuk '{keyword}'")
                        break
                    
                    # Delay antara request
                    time.sleep(5)  # tunggu 5 detik antara request
                    
                except Exception as e:
                    retry_count += 1
                    print(f"Error ({retry_count}/{max_retries}) untuk '{keyword}': {str(e)}")
                    print("Menunggu 30 detik sebelum mencoba lagi...")
                    time.sleep(30)  # tunggu lebih lama saat error
                    continue
            
            if retry_count >= max_retries:
                print(f"Gagal mengambil semua tweet untuk '{keyword}' setelah {max_retries} percobaan")
            
            # Tunggu sebentar sebelum pindah ke keyword berikutnya
            print("Menunggu 10 detik sebelum melanjutkan ke keyword berikutnya...")
            time.sleep(10)
    
    print(f"\nSelesai! Data telah disimpan ke {output_file}")

if __name__ == "__main__":
    main() 