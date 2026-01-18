import streamlit as st
from PIL import Image, ImageEnhance  # ImageEnhanceを追加
import io
from streamlit_image_comparison import image_comparison

# 1. アプリの名前を設定
st.set_page_config(page_title="簡単画像アップスケーリング", layout="wide")

st.title("🚀 簡単画像アップスケーリング")
st.write("複数の画像をまとめてアップロードし、鮮明に拡大・比較できます。")

# サイドバーに設定を集約
with st.sidebar:
    st.header("設定")
    # 拡大倍率の設定
    scale = st.slider("拡大倍率を選んでください", 1.0, 8.0, 4.0, 0.5)
    
    # 2. 鮮明にするためのシャープネス設定を追加
    st.subheader("画質調整")
    sharpness_value = st.slider("シャープネス（鮮明さ）", 1.0, 3.0, 1.5, 0.1)
    st.caption("値を大きくすると輪郭がくっきりしますが、上げすぎるとノイズが目立ちます。1.5前後がおすすめです。")

# 複数の画像を「一括変換」
uploaded_files = st.file_uploader(
    "画像をアップロードしてください（複数可）", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.divider()
    
    for uploaded_file in uploaded_files:
        # 画像読み込み
        img = Image.open(uploaded_file).convert("RGB")
        w, h = img.size
        
        # --- アップスケーリング処理 ---
        # 高品質なLANCZOS法でリサイズ
        new_size = (int(w * scale), int(h * scale))
        upscaled = img.resize(new_size, Image.LANCZOS)
        
        # --- 鮮明化処理 (Sharpness) ---
        enhancer = ImageEnhance.Sharpness(upscaled)
        upscaled = enhancer.enhance(sharpness_value)
        
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
            
    # 1. 完了メッセージの変更（風船を削除し、テキスト表示に）
    st.info("✅ アップスケーリング完了")