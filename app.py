import streamlit as st
import torch  # <---【修正點】這裡必須明確匯入 torch
from transformers import pipeline
import time

# --- 設定頁面配置 ---
st.set_page_config(
    page_title="AI vs Human 文章偵測器",
    page_icon="🕵️",
    layout="centered"
)

# --- 1. 載入模型 ---
@st.cache_resource
def load_model():
    """
    載入 Hugging Face 的預訓練模型。
    """
    # 建立分類管線
    # 這裡加入 truncation=True 以防止文章過長導致錯誤
    classifier = pipeline(
        "text-classification", 
        model="Hello-SimpleAI/chatgpt-detector-roberta",
        truncation=True, 
        max_length=512
    )
    return classifier

# --- 2. 側邊欄 (Sidebar) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=100)
    st.title("關於本工具")
    st.markdown("""
    這是一個基於 **Transformers** 模型的 AI 偵測工具。
    
    **功能特點：**
    - 🕵️ 自動偵測 AI 生成文本
    - 📊 顯示 AI 與 Human 的機率分佈
    
    **使用模型：**
    `Hello-SimpleAI/chatgpt-detector-roberta`
    """)
    st.markdown("---")
    st.caption("作業題目：Q1 — AI / Human 文章偵測器")

# --- 3. 主畫面 UI ---
st.title("🕵️ AI Content Detector")
st.markdown("貼上你的文章，讓 AI 判斷這段文字是由 **人類** 還是 **人工智慧** 寫的。")

# 文字輸入區
user_input = st.text_area("請輸入要分析的文本 (建議英文效果較佳)：", height=200, placeholder="在此貼上文章內容...")

col1, col2 = st.columns([1, 4])

if col1.button("開始分析", type="primary"):
    if not user_input.strip():
        st.warning("⚠️ 請輸入文字後再點擊分析！")
    else:
        with st.spinner('正在分析文本特徵...'):
            try:
                # 載入模型
                classifier = load_model()
                
                # 執行預測
                # truncation=True 在 load_model 已經設定，這裡直接傳入文字
                result = classifier(user_input)[0]
                
                time.sleep(0.5) # 模擬運算感

                # --- 4. 解析結果 ---
                label = result['label']
                score = result['score']

                # 邏輯處理：計算 AI 與 Human 的各自百分比
                # Hello-SimpleAI 模型的標籤通常是 'ChatGPT' 或 'Human'
                if label == 'ChatGPT':
                    ai_prob = score
                    human_prob = 1 - score
                else: # Label is Human
                    human_prob = score
                    ai_prob = 1 - score

                # 轉換為 0-100 的整數
                ai_percent = int(ai_prob * 100)
                human_percent = int(human_prob * 100)

                # --- 5. 顯示結果 UI ---
                st.markdown("---")
                st.subheader("分析結果")

                # 大數字指標
                m_col1, m_col2 = st.columns(2)
                m_col1.metric("🤖 AI 相似度", f"{ai_percent}%")
                m_col2.metric("👤 人類相似度", f"{human_percent}%")

                # 進度條
                st.write("AI Probability:")
                st.progress(ai_percent / 100, text=f"{ai_percent}% 可能為 AI 生成")
                
                st.write("Human Probability:")
                st.progress(human_percent / 100, text=f"{human_percent}% 可能為人類撰寫")

                # 結論判定
                st.markdown("### 📝 結論判定")
                if ai_percent > 80:
                    st.error("這篇文章 **極高機率** 是由 AI 生成的。")
                elif ai_percent > 50:
                    st.warning("這篇文章 **部分內容** 可能包含 AI 生成的痕跡。")
                else:
                    st.success("這篇文章 **極高機率** 是由人類撰寫的。")

                # --- 6. 詳細資訊 ---
                st.markdown("---")
                with st.expander("查看詳細統計數據"):
                    st.write(f"**字數統計：** {len(user_input)} 字元")
                    st.write(f"**原始標籤 (Label)：** {label}")
                    st.write(f"**原始分數 (Score)：** {score}")
                    st.json(result)

            except Exception as e:
                # 如果還有錯誤，會顯示詳細錯誤訊息
                st.error(f"發生錯誤：{e}")