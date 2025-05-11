import streamlit as st
import time
import base64
import os

# st.title("チャイムタイマー")


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


# タイマー表示
timer_placeholder = st.empty()

# time1 = st.text_input("タイマーの時間を入力してください（秒）", "5")
# time2 = st.text_input("タイマーの時間を入力してください（秒）", "10")
# time3 = st.text_input("タイマーの時間を入力してください（秒）", "20")

t1 = int(st.text_input("タイマーの時間を入力してください（秒）", "5"))
t2 = int(st.text_input("タイマーの時間を入力してください（秒）", "10"))
t3 = int(st.text_input("タイマーの時間を入力してください（秒）", "20"))

# チャイムファイル選択
wav_files = list_wav_files()
selected_wav = st.selectbox("チャイム音を選択してください", wav_files)


# ボタンを左寄せで横並びに（スタート、リセット、テスト）
col1, col2, col3 = st.columns([1,1,1])
with col1:
    start = st.button("スタート")
with col2:
    test = st.button("テスト")
with col3:
    reset = st.button("リセット")

# スタート処理
if start:
    st.session_state.start_time = time.time()
    st.session_state.chime_played = set()
    st.session_state.running = True
    st.write(f"⏲️ {t1}秒、{t2}秒、{t3}秒にチャイムが鳴ります")
    # st.markdown("<br>", unsafe_allow_html=True)
    # st.markdown(
    #     "<div style='font-size:12px;'>⏱ 5秒、10秒、15秒にチャイムが鳴ります</div>",
    #     unsafe_allow_html=True
    #     )

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

if st.session_state.running and st.session_state.start_time:
    chime = load_chime(selected_wav)
    while True:
        elapsed = int(time.time() - st.session_state.start_time)
        # if elapsed > 30:
        #     break

        # 経過時間を大きく表示
        timer_placeholder.markdown(
            f"<div style='font-size:110px'>🕒{elapsed//60:02d} 分 {elapsed%60:02d} 秒</div>",
            unsafe_allow_html=True
        )

        if elapsed in [t1, t2, t3] and elapsed not in st.session_state.chime_played:
            if elapsed==t1:
                st.markdown("<br>", unsafe_allow_html=True)
        
            st.write(f"🔔 {elapsed}秒経過：チャイム再生")    
            play_audio(chime)
            st.session_state.chime_played.add(elapsed)

        time.sleep(1)

    st.session_state.running = False
    # st.write("✅ 30秒経過：終了しました。")

# リセット直後は 0秒と表示
elif not st.session_state.running:
    timer_placeholder.markdown(
        "<div style='font-size:110px'>🕒 00 分 00 秒</div>",
        unsafe_allow_html=True
    )
