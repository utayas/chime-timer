import streamlit as st
import time
import base64
import os

st.title("チャイムタイマー")


# チャイムファイル一覧取得
def list_wav_files():
    return [f for f in os.listdir() if f.endswith(".wav")]

# チャイムファイル読み込み
def load_chime(filename):
    with open(filename, "rb") as f:
        return f.read()

# 音声再生関数（base64埋め込み）
def play_audio(audio_bytes):
    b64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
        <audio autoplay>
        <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# セッションステート初期化
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "chime_played" not in st.session_state:
    st.session_state.chime_played = set()
if "running" not in st.session_state:
    st.session_state.running = False


# チャイムファイル選択
wav_files = list_wav_files()
selected_wav = st.selectbox("チャイム音を選択してください", wav_files)


# ボタンを左寄せで横並びに（スタート、リセット、テスト）
col1, col2, col3 = st.columns([2,2,2])
with col1:
    start = st.button("スタート")
with col3:
    reset = st.button("リセット")
with col2:
    test = st.button("テスト")

st.markdown('</div>', unsafe_allow_html=True)


# スタート処理
if start:
    st.session_state.start_time = time.time()
    st.session_state.chime_played = set()
    st.session_state.running = True
    st.write("⏱ タイマー開始（5秒ごとにチャイムを鳴らします）")

# リセット処理
if reset:
    st.session_state.start_time = None
    st.session_state.chime_played = set()
    st.session_state.running = False

# テスト再生処理
if test:
    chime = load_chime(selected_wav)
    st.write(f"🎵 テスト再生中: {selected_wav}")
    play_audio(chime)

# タイマー表示
timer_placeholder = st.empty()

if st.session_state.running and st.session_state.start_time:
    chime = load_chime(selected_wav)
    while True:
        elapsed = int(time.time() - st.session_state.start_time)
        # if elapsed > 30:
        #     break

        # 経過時間を大きく表示
        timer_placeholder.markdown(
            f"<div style='font-size:60px'>🕒{elapsed//60:02d} 分 {elapsed%60:02d} 秒</div>",
            unsafe_allow_html=True
        )

        if elapsed in [5, 10, 15] and elapsed not in st.session_state.chime_played:
            if elapsed==5:
                st.markdown("<br>", unsafe_allow_html=True)
            st.write(f"🔔 {elapsed}秒経過：チャイム再生")
            play_audio(chime)
            st.session_state.chime_played.add(elapsed)

        time.sleep(1)

    st.session_state.running = False
    st.write("✅ 30秒経過：終了しました。")

# リセット直後は 0秒と表示
elif not st.session_state.running:
    timer_placeholder.markdown(
        "<div style='font-size:60px'>🕒 00 分 00 秒</div>",
        unsafe_allow_html=True
    )
