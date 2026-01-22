import streamlit as st
import pandas as pd
import re

# --- 1. KONFIGURASI HALAMAN & CSS (Latar Hitam & Border) ---
st.set_page_config(page_title="PLAT-CIPHER Crypto", layout="centered")

# CSS Kustom untuk Background Hitam dan Border
st.markdown(
    """
    <style>
    /* Mengubah warna background utama menjadi hitam */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Mengubah warna input text agar terlihat di background hitam */
    .stTextInput > div > div > input {
        color: #ffffff;
        background-color: #1e1e1e;
        border: 1px solid #444;
    }
    
    /* Membuat container utama memiliki border putih/abu-abu */
    .main-container {
        border: 2px solid #00FF00; /* Warna border hijau neon ala hacker/crypto */
        padding: 30px;
        border-radius: 10px;
        background-color: #111111;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
    }
    
    /* Styling tabel */
    .stDataFrame {
        border: 1px solid #333;
    }
    
    h1, h2, h3 {
        color: #00FF00 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 2. DATA REFERENSI (Sesuai Tabel Gambar)  ---
# Kita hardcode data ini agar sesuai persis dengan dokumen
db_plat = [
    {"Huruf": "A", "Kota": "Aceh", "Plat": "BL", "Angka": 4},
    {"Huruf": "B", "Kota": "Banyumas", "Plat": "R", "Angka": 8},
    {"Huruf": "C", "Kota": "Cirebon", "Plat": "E", "Angka": 7},
    {"Huruf": "D", "Kota": "Denpasar", "Plat": "DK", "Angka": 8},
    {"Huruf": "E", "Kota": "Ende", "Plat": "EB", "Angka": 4},
    {"Huruf": "F", "Kota": "Fakfak", "Plat": "PB", "Angka": 6},
    {"Huruf": "G", "Kota": "Garut", "Plat": "D", "Angka": 5},
    {"Huruf": "H", "Kota": "Hulu Sungai", "Plat": "DA", "Angka": 10},
    {"Huruf": "I", "Kota": "Intan Jaya", "Plat": "PA", "Angka": 9},
    {"Huruf": "J", "Kota": "Jakarta", "Plat": "B", "Angka": 7},
    {"Huruf": "K", "Kota": "Kediri", "Plat": "AG", "Angka": 6},
    {"Huruf": "L", "Kota": "Lampung", "Plat": "BE", "Angka": 7},
    {"Huruf": "M", "Kota": "Medan", "Plat": "BK", "Angka": 5},
    {"Huruf": "N", "Kota": "Ngawi", "Plat": "AE", "Angka": 5},
    {"Huruf": "O", "Kota": "Oleh-oleh", "Plat": "DB", "Angka": 10},
    {"Huruf": "P", "Kota": "Palembang", "Plat": "BG", "Angka": 9},
    {"Huruf": "Q", "Kota": "-", "Plat": "Q", "Angka": 0},
    {"Huruf": "R", "Kota": "Riau", "Plat": "BM", "Angka": 4},
    {"Huruf": "S", "Kota": "Surabaya", "Plat": "L", "Angka": 8},
    {"Huruf": "T", "Kota": "Tegal", "Plat": "G", "Angka": 5},
    {"Huruf": "U", "Kota": "Ujung Pandang", "Plat": "DD", "Angka": 12},
    {"Huruf": "V", "Kota": "-", "Plat": "V", "Angka": 0},
    {"Huruf": "W", "Kota": "Wonogiri", "Plat": "AD", "Angka": 8},
    {"Huruf": "X", "Kota": "-", "Plat": "X", "Angka": 0},
    {"Huruf": "Y", "Kota": "Yogyakarta", "Plat": "AB", "Angka": 10},
    {"Huruf": "Z", "Kota": "Z", "Plat": "Z", "Angka": 0},
]

df_ref = pd.DataFrame(db_plat)

# --- 3. FUNGSI LOGIKA PLAT-CIPHER ---

def enkripsi_plat_cipher(plaintext):
    """
    Proses Enkripsi:
    1. Cari Huruf -> Plat
    2. Aturan Kapitalisasi: Jika Plat 2 huruf (ex: AB) -> aB. Jika 1 huruf (ex: R) -> R.
    3. Gabung dengan Angka (Jumlah Kata/Huruf Kota).
    """
    ciphertext = ""
    steps_log = [] # Untuk menyimpan log proses agar user paham
    
    # Bersihkan input, ambil huruf saja, uppercase
    clean_text = ''.join(filter(str.isalpha, plaintext.upper()))
    
    for char in clean_text:
        # Cari data di tabel referensi
        row = df_ref[df_ref['Huruf'] == char]
        
        if not row.empty:
            plat_awal = row.iloc[0]['Plat']
            angka = row.iloc[0]['Angka']
            
            # --- Aturan Kapitalisasi  ---
            plat_jadi = plat_awal
            if len(plat_awal) == 2:
                # Huruf pertama kecil, huruf kedua besar (Contoh: BL -> bL)
                plat_jadi = plat_awal[0].lower() + plat_awal[1].upper()
            else:
                # Huruf satu tetap (Contoh: R -> R, Z -> Z)
                plat_jadi = plat_awal
            
            # --- Penggabungan ---
            segment = f"{plat_jadi}{angka}"
            ciphertext += segment
            
            steps_log.append(f"{char} -> {plat_awal} -> {plat_jadi} + {angka} = {segment}")
        else:
            # Jika karakter tidak ditemukan (jarang terjadi jika input sudah difilter A-Z)
            ciphertext += char 

    return ciphertext, steps_log

def dekripsi_plat_cipher(ciphertext):
    """
    Proses Dekripsi:
    1. Parsing string menjadi chunk (Plat + Angka).
    2. Normalisasi Plat (bL -> BL).
    3. Cari kombinasi Plat & Angka di database untuk dapatkan Huruf asli.
    """
    plaintext = ""
    steps_log = []
    
    # Regex untuk memisahkan huruf (plat) dan angka
    # Pola: ([a-zA-Z]+) menangkap huruf (bisa bL, R, aB), (\d+) menangkap angka
    tokens = re.findall(r'([a-zA-Z]+)(\d+)', ciphertext)
    
    for plat_raw, angka_str in tokens:
        angka = int(angka_str)
        
        # --- Normalisasi Kapitalisasi ---
        # Kita harus mengubah format aB kembali menjadi AB untuk dicocokkan dengan database
        plat_normal = plat_raw.upper()
        
        # Cari di database: Syarat Plat harus sama DAN Angka harus sama
        match = df_ref[
            (df_ref['Plat'] == plat_normal) & 
            (df_ref['Angka'] == angka)
        ]
        
        if not match.empty:
            huruf_asli = match.iloc[0]['Huruf']
            plaintext += huruf_asli
            steps_log.append(f"{plat_raw}{angka} -> Plat: {plat_normal}, Angka: {angka} -> Huruf: {huruf_asli}")
        else:
            plaintext += "?" # Indikator jika tidak ketemu
            steps_log.append(f"{plat_raw}{angka} -> Tidak ditemukan di database")
            
    return plaintext, steps_log

# --- 4. TAMPILAN UTAMA (CONTAINER) ---

# Menggunakan HTML container kustom agar bisa diberi border sesuai request
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.title("🔒 PLAT-CIPHER Generator")
st.write("Aplikasi Kriptografi Berbasis Kode Plat Nomor & Wilayah")
st.markdown("---")

# Tampilkan Tabel Referensi (Expander)
with st.expander("📖 Lihat Tabel Referensi (Kunci)"):
    st.dataframe(df_ref, use_container_width=True)

# Tab Navigasi
tab1, tab2 = st.tabs(["🔐 ENKRIPSI", "🔓 DESKRIPSI"])

# --- TAB ENKRIPSI ---
with tab1:
    st.subheader("Proses Enkripsi")
    st.write("Mengubah Teks Asli menjadi Kode Plat.")
    
    input_text = st.text_input("Masukkan Plaintext (Huruf A-Z):", placeholder="Contoh: AMIKOM")
    
    if st.button("Enkripsi Sekarang", type="primary"):
        if input_text:
            hasil_enc, logs = enkripsi_plat_cipher(input_text)
            
            st.success("Berhasil!")
            st.markdown(f"### Ciphertext: **`{hasil_enc}`**")
            
            with st.expander("Lihat Detail Proses"):
                for log in logs:
                    st.text(log)
        else:
            st.warning("Mohon masukkan teks terlebih dahulu.")

# --- TAB DEKRIPSI ---
with tab2:
    st.subheader("Proses Dekripsi")
    st.write("Mengembalikan Kode Plat menjadi Teks Asli.")
    
    input_cipher = st.text_input("Masukkan Ciphertext:", placeholder="Contoh: bL4bK5pA9aG6dB10bK5")
    
    if st.button("Dekripsi Sekarang"):
        if input_cipher:
            hasil_dec, logs_dec = dekripsi_plat_cipher(input_cipher)
            
            st.success("Berhasil!")
            st.markdown(f"### Plaintext: **`{hasil_dec}`**")
            
            with st.expander("Lihat Detail Proses"):
                for log in logs_dec:
                    st.text(log)
        else:
            st.warning("Mohon masukkan ciphertext terlebih dahulu.")

st.markdown('</div>', unsafe_allow_html=True) # Tutup main-container
st.markdown("<br><center><small>Dibuat berdasarkan Modul PLAT-CHIPER</small></center>", unsafe_allow_html=True)
