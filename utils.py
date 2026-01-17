import requests
from bs4 import BeautifulSoup
import re
import json

def extract_reel_id(url):
    """Ekstrak ID Reel dari URL"""
    pattern = r"https://www\.facebook\.com/reel/(\d+)"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_video_download_url(reel_id):
    """
    Fungsi ini mencoba mendapatkan URL download video
    Note: Ini adalah pendekatan dasar, mungkin tidak selalu berhasil karena proteksi Facebook
    """
    try:
        # Metode 1: Coba scraping dasar
        url = f"https://www.facebook.com/reel/{reel_id}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Cari video URL dalam source HTML
        video_patterns = [
            r'video_src":"([^"]+)"',
            r'hd_src":"([^"]+)"',
            r'sd_src":"([^"]+)"',
            r'"url":"([^"]+\.mp4[^"]*)"'
        ]
        
        content = str(soup)
        for pattern in video_patterns:
            matches = re.findall(pattern, content)
            if matches:
                # Ambil URL tertinggi kualitas
                return matches[0].replace('\\u00253A', ':').replace('\\u00252F', '/')
                
        return None
        
    except Exception as e:
        print(f"Error getting download URL: {e}")
        return None

def process_multiple_urls(urls_text):
    """Proses multiple URLs dan ekstrak ID"""
    pattern = r"https://www\.facebook\.com/reel/\d+"
    found_links = re.findall(pattern, urls_text)
    unique_links = list(set(found_links))
    
    results = []
    for link in unique_links:
        reel_id = extract_reel_id(link)
        if reel_id:
            download_url = get_video_download_url(reel_id)
            results.append({
                'id': reel_id,
                'original_url': link,
                'download_url': download_url,
                'status': 'Success' if download_url else 'Failed to get download URL'
            })
        else:
            results.append({
                'id': 'Unknown',
                'original_url': link,
                'download_url': None,
                'status': 'Invalid URL format'
            })
    
    return results
