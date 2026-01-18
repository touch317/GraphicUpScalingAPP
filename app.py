import streamlit as st
from PIL import Image, ImageEnhance
import io
from streamlit_image_comparison import image_comparison

# 1. アプリの設定（名前とレイアウト）
st.set_page_config(page_title="簡単画像アップスケーリング", layout="wide")

st.title("🚀 簡単画像アップスケーリング")
st.write("複数の画像をまとめてアップロードし、鮮明に拡大・比較できます。")

# --- 2. サイドバーに設定と使い方を追加 ---
with st.sidebar:
    st.header("⚙️ 設定")
    # 拡大倍率の設定
    scale = st.slider("拡大倍率を選んでください", 1.0, 8.0, 4.0, 0.5)
    
    # 鮮明にするためのシャープネス設定
    st.subheader("画質調整")
    sharpness_value = st.slider("シャープネス（鮮明さ）", 1.0, 3.0, 1.5, 0.1)
    st.caption("1.5〜2.0に設定すると輪郭がくっきりします。")

    st.divider() # 区切り線
    
    # サイドバーに「使い方」を追加
    st.subheader("📖 使い方")
    st.markdown("""
    1. 中央のエリアに画像をアップロード（複数可）。
    2. 左のスライダーで倍率と鮮明さを調整。
    3. 中央のスライダーを動かして仕上がりを確認。
    4. 各画像のボタンからダウンロード！
    """)

# 複数の画像を「一括変換」
uploaded_files = st.file_uploader(
    "画像をアップロードしてください（複数可）", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.divider()
    
    for uploaded_file in uploaded_files:
        # --- 1. 処理中の「待ち時間」を表示（スピナー） ---
        with st.spinner(f"「{uploaded_file.name}」をアップスケーリング中..."):
            # 画像読み込み
            img = Image.open(uploaded_file).convert("RGB")
            w, h = img.size
            
            # 高品質なLANCZOS法でリサイズ
            new_size = (int(w * scale), int(h * scale))
            upscaled = img.resize(new_size, Image.LANCZOS)
            
            # 鮮明化処理 (Sharpness)
            enhancer = ImageEnhance.Sharpness(upscaled)
            upscaled = enhancer.enhance(sharpness_value)
            
            # 処理が終わるとスピナーが消え、以下の表示が始まります
        
        # 画面表示用のコンテナ
        with st.expander(f"📄 {uploaded_file.name} の処理結果", expanded=True):
            # 比較機能
            image_comparison(
                img1=img,
                img2=upscaled,
                label1="元画像",
                label2=f"{scale}倍拡大・鮮明化後",
                width=700,
                starting_position=50,
                show_labels=True,
                make_responsive=True,
                in_memory=True
            )
            
            # ダウンロード用データの準備
            buf = io.BytesIO()
            upscaled.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label=f"{uploaded_file.name} をダウンロード",
                data=byte_im,
                file_name=f"upscaled_{scale}x_{uploaded_file.name}",
                mime="image/png",
                key=uploaded_file.name
            )
            
    # 完了メッセージの表示（風船なしのシンプル版）
    st.info("✅ アップスケーリング完了")
