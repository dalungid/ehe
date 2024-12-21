import os
import requests
from pytube import YouTube
from ssstik import SsstikIO  # Asumsikan kode TikTok telah disimpan sebagai ssstik.py
import ffmpeg
import random
import re


def generate_random_color():
    """Menghasilkan warna acak dalam format hexadecimal (#RRGGBB)."""
    return '#' + ''.join(random.choices('0123456789ABCDEF', k=6))


def is_valid_hex_color(color):
    """Memeriksa apakah input adalah kode warna hexadecimal yang valid."""
    hex_color_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
    return bool(hex_color_pattern.match(color))


def print_tutorial_for_tool(tool_name):
    """Menampilkan tutorial spesifik untuk setiap tool."""
    tutorials = {
        "Unduh Video YouTube": """
        Tutorial: Cara Mengunduh Video YouTube
        1. Masukkan URL video YouTube yang ingin diunduh.
        2. Video akan otomatis diunduh ke folder 'downloads'.
        3. Anda dapat menambahkan pengeditan setelah video diunduh.
        """,
        "Unduh Video TikTok": """
        Tutorial: Cara Mengunduh Video TikTok
        1. Masukkan URL video TikTok yang ingin diunduh.
        2. Video akan otomatis diunduh ke folder 'downloads'.
        3. Anda dapat menambahkan pengeditan setelah video diunduh.
        """,
        "Tambah Border": """
        Tutorial: Cara Menambahkan Border
        1. Pilih warna border yang diinginkan.
        2. Pilih ketebalan border (dalam piksel).
        3. Border akan diterapkan ke video yang telah diunduh.
        """,
        "Tambah Overlay": """
        Tutorial: Cara Menambahkan Overlay
        1. Masukkan URL atau path file gambar/video untuk overlay.
        2. Pilih posisi overlay pada video (misalnya: top-left, center, bottom-right).
        3. Overlay akan diterapkan di atas video yang telah diunduh.
        """,
        "Edit Metadata": """
        Tutorial: Cara Mengedit Metadata
        1. Setelah video diunduh dan diedit, Anda dapat memperbarui metadata video.
        2. Masukkan judul video, nama pengarang, dan deskripsi.
        3. Metadata akan diperbarui pada video final.
        """,
        "Buat Kumpulan Video": """
        Tutorial: Cara Membuat Kumpulan Video
        1. Masukkan URL video (YouTube atau TikTok) yang ingin digabungkan.
        2. Anda dapat menambahkan beberapa URL dan menggabungkan video-video tersebut.
        3. Video hasil gabungan akan disimpan sebagai satu file.
        """,
        "Proses Bulk dari list.txt": """
        Tutorial: Proses Bulk Video
        1. Siapkan file 'list.txt' yang berisi daftar URL video.
        2. Program akan mengunduh dan mengedit video-video yang terdaftar di file tersebut.
        3. Pastikan file list.txt sudah terisi dengan benar.
        """
    }
    print(tutorials.get(tool_name, "Tidak ada tutorial untuk tool ini."))


def main_menu():
    """Menu utama dengan penjelasan fitur dan pemilihan tool."""
    while True:
        print("\n==================== Menu Utama ====================")
        print("1. Unduh Video YouTube")
        print("2. Unduh Video TikTok")
        print("3. Tambah Border pada Video")
        print("4. Tambah Overlay pada Video")
        print("5. Edit Metadata Video")
        print("6. Buat Kumpulan Video (MEME, Kumpulan Video Lucu)")
        print("7. Proses Bulk dari list.txt")
        print("8. Lihat Tutorial")
        print("9. Keluar")
        print("=====================================================")

        choice = input("Pilih opsi (1-9): ").strip()

        if choice == "1":
            url = input("Masukkan URL video YouTube: ").strip()
            download_video_and_edit(url, "YouTube")
        elif choice == "2":
            url = input("Masukkan URL video TikTok: ").strip()
            download_video_and_edit(url, "TikTok")
        elif choice == "3":
            video_path = input("Masukkan path video yang akan diberi border: ").strip()
            is_random_color = input("Gunakan warna acak? (yes/no): ").strip().lower() == "yes"
            if is_random_color:
                border_color = generate_random_color()
            else:
                border_color = input("Pilih warna border (nama atau kode warna #RRGGBB, default: black): ").strip() or "black"
            border_thickness = int(input("Pilih ketebalan border (angka, default: 10): ").strip() or 10)
            add_border(video_path, border_color, border_thickness)
        elif choice == "7":
            txt_file = input("Masukkan path file list.txt (default: list.txt): ").strip() or "list.txt"
            is_random_color = input("Apakah Anda ingin menggunakan warna acak untuk border? (yes/no): ").strip().lower() == "yes"
            process_bulk_videos_from_list(txt_file, is_random_color)
        elif choice == "9":
            print("Keluar dari aplikasi...")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")


def download_video_and_edit(url, platform):
    """Mengunduh dan mengedit video berdasarkan URL platform."""
    if platform == "YouTube":
        video_file, title = download_youtube_video(url)
    elif platform == "TikTok":
        video_file, title = download_tiktok_video(url)
    
    if video_file:
        print(f"Video {platform} berhasil diunduh: {video_file}")
        
        # Tambahkan pengeditan jika diperlukan
        border_color = input("Pilih warna border (default: black): ").strip() or "black"
        border_thickness = int(input("Pilih ketebalan border (angka, default: 10): ").strip() or 10)
        video_file = add_border(video_file, border_color, border_thickness)

        overlay_url = input("Masukkan URL atau path file overlay (gambar/video): ").strip()
        position = input("Pilih posisi overlay (top-left, top-right, center, bottom-left, bottom-right): ").strip() or "center"
        video_file = add_overlay(video_file, overlay_url, position)
        
        title = input("Masukkan judul video: ").strip()
        author = input("Masukkan nama pengarang: ").strip()
        description = input("Masukkan deskripsi video: ").strip()
        video_file = update_metadata(video_file, title, author, description)

        print(f"Proses selesai. Video disimpan di: {video_file}")


def download_youtube_video(url, output_path="downloads"):
    """Mengunduh video dari YouTube."""
    try:
        os.makedirs(output_path, exist_ok=True)
        yt = YouTube(url)
        video_stream = yt.streams.filter(progressive=True, file_extension="mp4").first()
        output_file = video_stream.download(output_path)
        print(f"Video YouTube berhasil diunduh: {output_file}")
        return output_file, yt.title
    except Exception as e:
        print(f"Kesalahan saat mengunduh video YouTube: {e}")
        return None, None


def download_tiktok_video(url, output_path="downloads"):
    """Mengunduh video dari TikTok."""
    try:
        os.makedirs(output_path, exist_ok=True)
        ssstik = SsstikIO()
        downloads = ssstik.get_media(url)
        video_file = downloads[0].video  # Mendapatkan URL video dari hasil download
        response = requests.get(video_file)
        
        output_file = os.path.join(output_path, "tiktok_video.mp4")
        with open(output_file, 'wb') as f:
            f.write(response.content)
        
        print(f"Video TikTok berhasil diunduh: {output_file}")
        return output_file, "TikTok Video"
    except Exception as e:
        print(f"Kesalahan saat mengunduh video TikTok: {e}")
        return None, None


def add_border(video_path, color="black", thickness=10):
    """Menambahkan border pada video."""
    output_path = f"output_with_border_{os.path.basename(video_path)}"
    ffmpeg.input(video_path).filter('border', color=color, thickness=thickness).output(output_path).run()
    print(f"Border berhasil ditambahkan. Video disimpan di: {output_path}")
    return output_path


def add_overlay(video_path, overlay_url, position="center"):
    """Menambahkan overlay pada video."""
    overlay_path = download_overlay(overlay_url)  # Fungsi untuk mengunduh overlay dari URL
    output_path = f"output_with_overlay_{os.path.basename(video_path)}"
    ffmpeg.input(video_path).output(output_path, vf=f"movie={overlay_path} [watermark]; [in][watermark] overlay={position} [out]").run()
    print(f"Overlay berhasil ditambahkan. Video disimpan di: {output_path}")
    return output_path


def download_overlay(overlay_url):
    """Mengunduh file overlay (gambar/video) dari URL."""
    if overlay_url.startswith("http"):
        response = requests.get(overlay_url)
        overlay_path = "overlay_temp.mp4" if "video" in response.headers.get("content-type", "") else "overlay_temp.png"
        with open(overlay_path, "wb") as f:
            f.write(response.content)
        return overlay_path
    else:
        return overlay_url


def update_metadata(video_path, title, author, description):
    """Memperbarui metadata pada video."""
    output_path = f"final_{os.path.basename(video_path)}"
    ffmpeg.input(video_path, metadata=f"title={title}", metadata=f"author={author}", metadata=f"description={description}").output(output_path).run()
    print(f"Metadata berhasil diperbarui. Video disimpan di: {output_path}")
    return output_path


if __name__ == "__main__":
    main_menu()
