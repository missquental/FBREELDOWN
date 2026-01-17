import streamlit as st
import requests
from utils import process_multiple_urls, extract_reel_id, get_video_download_url

# Konfigurasi halaman
st.set_page_config(
    page_title="Facebook Reels Downloader",
    page_icon="📥",
    layout="wide"
)

# CSS untuk styling
st.markdown("""
<style>
.header {
    text-align: center;
    padding: 2rem 0;
}
.feature-card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.stButton>button {
    background-color: #1877f2;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #166fe5;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header">', unsafe_allow_html=True)
st.title("📥 Facebook Reels Downloader")
st.subheader("Download video Reels Facebook dengan mudah!")
st.markdown('</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["🎯 Single URL", "📋 Multiple URLs"])

with tab1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### 🔗 Masukkan URL Reels Facebook")
    single_url = st.text_input("", 
                              placeholder="https://www.facebook.com/reel/123456789",
                              key="single_url")
    
    if st.button("📥 Download Video", key="single_download"):
        if single_url:
            with st.spinner("Memproses..."):
                reel_id = extract_reel_id(single_url)
                if reel_id:
                    download_url = get_video_download_url(reel_id)
                    if download_url:
                        st.success("✅ Video ditemukan!")
                        st.video(download_url)
                        
                        # Tombol download
                        st.markdown(f"[⬇️ Download Video]({download_url})")
                        
                        # Info tambahan
                        st.info(f"**Reel ID:** {reel_id}")
                        st.info("**Note:** Jika video tidak bisa diputar, klik tombol download di atas.")
                    else:
                        st.error("❌ Gagal mendapatkan URL download. Video mungkin dilindungi atau tidak tersedia.")
                else:
                    st.error("❌ Format URL tidak valid. Pastikan URL berformat: https://www.facebook.com/reel/ID")
        else:
            st.warning("⚠️ Harap masukkan URL terlebih dahulu.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Masukkan Banyak URL (satu per baris)")
    multiple_urls = st.text_area("", 
                                placeholder="https://www.facebook.com/reel/123456789\nhttps://www.facebook.com/reel/987654321",
                                height=200,
                                key="multiple_urls")
    
    if st.button("📊 Proses Semua URL", key="multiple_process"):
        if multiple_urls:
            with st.spinner("Memproses semua URL..."):
                results = process_multiple_urls(multiple_urls)
                
                if results:
                    st.success(f"✅ Diproses {len(results)} URL")
                    
                    # Tampilkan hasil dalam tabel
                    st.markdown("### 📊 Hasil Pemrosesan")
                    for i, result in enumerate(results, 1):
                        st.markdown(f"#### #{i} - Reel ID: {result['id']}")
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**URL Asli:** {result['original_url']}")
                            st.markdown(f"**Status:** {result['status']}")
                            
                        with col2:
                            if result['download_url']:
                                st.markdown(f"[⬇️ Download]({result['download_url']})")
                                if st.button("▶️ Play", key=f"play_{i}"):
                                    st.video(result['download_url'])
                            else:
                                st.markdown("❌ Tidak tersedia")
                        
                        st.markdown("---")
                    
                    # Opsi download hasil
                    result_text = "\n".join([f"{r['original_url']} | Status: {r['status']}" for r in results])
                    st.download_button(
                        label="💾 Download Hasil (TXT)",
                        data=result_text,
                        file_name="facebook_reels_results.txt",
                        mime="text/plain"
                    )
                else:
                    st.info("🔍 Tidak ada URL valid ditemukan.")
        else:
            st.warning("⚠️ Harap masukkan URL terlebih dahulu.")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>ℹ️ Catatan Penting:</strong></p>
    <p>Aplikasi ini hanya untuk tujuan edukasi. Pastikan Anda memiliki hak untuk mendownload konten tersebut.</p>
    <p>Karena pembatasan Facebook, beberapa video mungkin tidak bisa didownload secara langsung.</p>
</div>
""", unsafe_allow_html=True)
