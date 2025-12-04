DEMO：

📘 AI vs Human Text Detector (AI 生成文本偵測器)
📝 專案簡介 (Project Overview)
隨著大型語言模型（LLM）如 ChatGPT 的普及，區分「人工撰寫」與「AI 生成」的內容變得日益重要且具挑戰性。本專案旨在開發一個簡單、直觀且高效的網頁應用程式，利用深度學習技術來協助使用者辨識文本的來源。透過此工具，使用者可以快速分析文章的語意特徵，判斷其是否由人工智慧生成。

🛠️ 技術架構 (Technology Stack)
本專案基於 Python 開發，整合了以下核心技術：

前端介面：使用 Streamlit 框架建構，提供使用者友善的互動式 UI，包含進度條視覺化與指標儀表板。

核心模型：採用 Hugging Face Transformers 函式庫，並搭載 PyTorch 深度學習框架。

預訓練模型：選用 Hello-SimpleAI/chatgpt-detector-roberta。這是一個基於 RoBERTa 架構的模型，經過特定資料集（ChatGPT 生成文本 vs 人類文本）微調（Fine-tuning），在偵測生成式 AI 內容上具有較高的準確度。

✨ 核心功能 (Key Features)
即時判讀：輸入文本後，模型即時進行推論，並輸出「AI 生成」與「人類撰寫」的機率百分比。

視覺化呈現：仿照商用偵測工具（如 JustDone），以動態進度條和顏色警示（綠/黃/紅）來呈現判斷結果，讓資訊一目了然。

詳細統計：提供字數統計、原始模型標籤（Label）及信賴分數（Confidence Score），供進階分析參考。
