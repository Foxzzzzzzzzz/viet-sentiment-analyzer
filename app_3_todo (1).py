"""
BÀI TẬP: Morphology & Sentiment tiếng Việt với underthesea
===========================================================
Sinh viên cần hoàn thành các phần đánh dấu TODO bên dưới.

Yêu cầu:
  1) Dùng underthesea.word_tokenize thay cho simple_tokenize (split đơn giản).
  2) Dùng underthesea.sentiment thay cho rule-based sentiment.
  3) So sánh kết quả giữa 2 cách (rule-based vs underthesea).

Cài đặt: pip install underthesea streamlit
Chạy:    streamlit run app_3_todo.py
"""

import re
from collections import Counter

import streamlit as st

# TODO 1: Import word_tokenize và sentiment từ thư viện underthesea
# ---- ĐÃ HOÀN THÀNH TODO 1 ----
from underthesea import word_tokenize, sentiment
# ------------------------------


# ========= CẤU HÌNH TỪ VỰNG MẪU =========

PREFIX_MEANINGS = {
    "bất": "phủ định / không",
    "phi": "trái với / không theo",
    "tái": "lặp lại / làm lại",
    "siêu": "rất / vượt trội",
    "phụ": "thêm / phụ trợ",
}

POSITIVE_PHRASES = [
    "chạy nhanh", "chạy_nhanh", "chơi game mượt", "chơi_game_mượt",
    "màn hình đẹp", "màn_hình_đẹp", "đẹp quá", "rất đẹp",
    "đẹp_lung_linh", "siêu đẹp", "hài lòng", "rất hài lòng",
]

NEGATIVE_PHRASES = [
    "chạy chậm", "chạy_chậm", "lag", "giật lag", "giật_lag",
    "lâu kinh", "pin yếu", "pin_yếu", "tụt pin", "tụt_pin",
    "hao pin", "hao_pin", "tụt kinh khủng", "tụt_kinh_khủng",
    "máy nóng", "máy_hơi_nóng", "camera chụp xấu", "camera_chụp_xấu",
    "xấu quá",
]

EXAMPLE_TEXT = (
    "Máy chạy nhanh, chơi game mượt, màn hình đẹp nhưng pin tụt kinh khủng, "
    "sạc hoài luôn. Thỉnh thoảng hơi lag nữa. Mình khá hài lòng nhưng pin yếu quá."
)


# ========= HÀM TIỆN ÍCH =========

def normalize_text(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def simple_tokenize(text: str):
    """Tokenize đơn giản bằng split() — dùng làm baseline so sánh."""
    return text.split()


def underthesea_tokenize(text: str):
    """
    TODO 2: Dùng word_tokenize từ underthesea để tách từ tiếng Việt.
    ---- ĐÃ HOÀN THÀNH TODO 2 ----

    Giải thích:
      - word_tokenize(text) trả về list token, ví dụ: ['màn_hình', 'đẹp', 'quá']
        (underthesea nối từ ghép bằng dấu gạch dưới '_')
      - word_tokenize(text, format="text") trả về chuỗi: 'màn_hình đẹp quá'

    Trả về tuple (tokens_list, tokens_text):
      - tokens_list: list token
      - tokens_text: chuỗi token dạng text
    """
    tokens_list = word_tokenize(text)                      # list token
    tokens_text = word_tokenize(text, format="text")       # chuỗi token
    return tokens_list, tokens_text


def safe_sentiment(text: str) -> str:
    """
    TODO 3: Gọi underthesea.sentiment(text) để lấy nhãn cảm xúc.
    ---- ĐÃ HOÀN THÀNH TODO 3 ----

    Giải thích:
      - sentiment(text) có thể trả về string 'positive'/'negative'/'neutral'
        hoặc list/tuple tuỳ phiên bản underthesea.
      - Nếu trả về list/tuple thì lấy phần tử đầu tiên.
      - Bọc trong try/except để tránh crash khi chưa tải model.
    """
    try:
        result = sentiment(text)
        # Một số phiên bản underthesea trả về list hoặc tuple
        if isinstance(result, (list, tuple)):
            return str(result[0])
        return str(result)
    except Exception as e:
        return f"Lỗi: {e}"


def detect_prefixes(tokens, prefixes: dict) -> Counter:
    counts = Counter()
    for tok in tokens:
        t = re.sub(
            r"[^\w_áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệ"
            r"íìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữự"
            r"ýỳỷỹỵđ]",
            "",
            tok.lower(),
        )
        for pref in prefixes:
            if t.startswith(pref):
                counts[pref] += 1
    return counts


def detect_phrases(text: str, phrases: list) -> Counter:
    counts = Counter()
    for p in phrases:
        if not p:
            continue
        matches = re.findall(re.escape(p), text)
        if matches:
            counts[p] = len(matches)
    return counts


def overall_sentiment(pos_count: int, neg_count: int) -> str:
    if pos_count == 0 and neg_count == 0:
        return "KHÔNG RÕ / TRUNG TÍNH"
    if pos_count > neg_count:
        return "TÍCH CỰC"
    elif neg_count > pos_count:
        return "TIÊU CỰC"
    return "TRUNG TÍNH / LẪN LỘN"


# ========= GIAO DIỆN STREAMLIT =========

st.set_page_config(
    page_title="Morphology & Sentiment tiếng Việt (BÀI TẬP)",
    page_icon="🧬",
    layout="wide",
)

st.title("🧬 BÀI TẬP — Morphology & Sentiment tiếng Việt")

st.markdown(
    """
**Sinh viên cần hoàn thành 4 TODO trong file này:**

| TODO | Nội dung | Trạng thái |
|------|----------|------------|
| TODO 1 | Import `word_tokenize`, `sentiment` từ `underthesea` | ✅ Hoàn thành |
| TODO 2 | Viết hàm `underthesea_tokenize()` dùng `word_tokenize` | ✅ Hoàn thành |
| TODO 3 | Viết hàm `safe_sentiment()` dùng `sentiment` | ✅ Hoàn thành |
| TODO 4 | Hiển thị kết quả underthesea tokenize & sentiment trên giao diện | ✅ Hoàn thành |
"""
)

col_left, col_right = st.columns([1.1, 1.6])

with col_left:
    st.subheader("Nhập review / comment tiếng Việt")

    def _paste_example():
        st.session_state["input_text"] = EXAMPLE_TEXT

    st.button("Dán ví dụ gợi ý", on_click=_paste_example)

    text = st.text_area(
        "Văn bản",
        key="input_text",
        height=200,
        placeholder="Ví dụ: Máy chạy nhanh, chơi game mượt, màn hình đẹp nhưng pin tụt kinh khủng...",
    )

    analyze_btn = st.button("Phân tích Morphology & Sentiment")

with col_right:
    st.subheader("Kết quả")

    if not text.strip():
        st.info("Hãy nhập một đoạn văn rồi bấm **Phân tích**.")
    elif analyze_btn:
        norm_text = normalize_text(text)

        # ============================================================
        # PHẦN A — Tokenization: so sánh split() vs underthesea
        # ============================================================
        st.markdown("### 1️⃣ Tokenization — So sánh 2 cách")

        # --- Cách 1: split đơn giản (đã có sẵn) ---
        tokens_simple = simple_tokenize(norm_text)
        st.markdown("**Cách 1 — split() đơn giản:**")
        st.code(" | ".join(tokens_simple))
        st.caption(f"Số token: {len(tokens_simple)}")

        # --- Cách 2: underthesea word_tokenize ---
        st.markdown("**Cách 2 — underthesea `word_tokenize`:**")

        # TODO 4a: Gọi underthesea_tokenize(text) và hiển thị kết quả.
        # ---- ĐÃ HOÀN THÀNH TODO 4a ----
        tokens_list, tokens_text = underthesea_tokenize(text)
        st.code(" | ".join(tokens_list))
        st.write("Dạng text:", tokens_text)
        st.caption(
            f"Số token: {len(tokens_list)}  "
            f"(split: {len(tokens_simple)}, underthesea: {len(tokens_list)} — "
            f"{'underthesea nhận ra ít token hơn vì gộp từ ghép' if len(tokens_list) < len(tokens_simple) else 'số lượng tương đương'})"
        )
        tokens_ut = tokens_list   # dùng token underthesea cho các bước sau
        # --------------------------------

        # ============================================================
        # PHẦN B — Tiền tố Hán-Việt (dùng token từ underthesea)
        # ============================================================
        st.markdown("### 2️⃣ Yếu tố Hán‑Việt dạng 'tiền tố nghĩa'")
        prefix_counts = detect_prefixes(tokens_ut, PREFIX_MEANINGS)
        if prefix_counts:
            for pref, c in prefix_counts.items():
                meaning = PREFIX_MEANINGS.get(pref, "")
                st.write(f"- `{pref}`: **{c}** lần – nghĩa: *{meaning}*")
        else:
            st.write("_Chưa thấy tiền tố mẫu. Thử thêm từ như `bất_cẩn`, `phi_lý`, `siêu_rẻ`._")

        # ============================================================
        # PHẦN C — Sentiment: so sánh rule-based vs underthesea
        # ============================================================
        st.markdown("### 3️⃣ Sentiment — So sánh 2 cách")

        # --- Cách 1: Rule-based (đã có sẵn) — từng bước ---
        st.markdown("#### 🔧 Cách 1 — Rule-based (từng bước)")

        pos_counts = detect_phrases(norm_text, POSITIVE_PHRASES)
        neg_counts = detect_phrases(norm_text, NEGATIVE_PHRASES)
        pos_total = sum(pos_counts.values())
        neg_total = sum(neg_counts.values())
        total_phrases = pos_total + neg_total

        # Bước 1: Liệt kê cụm
        st.markdown("##### Bước 1 — Phát hiện cụm cảm xúc")
        col_pos, col_neg = st.columns(2)
        with col_pos:
            st.markdown("🟢 **Cụm tích cực**")
            if pos_counts:
                for p, c in pos_counts.items():
                    st.write(f"- `{p}` × {c}")
            else:
                st.write("_Không tìm thấy_")
        with col_neg:
            st.markdown("🔴 **Cụm tiêu cực**")
            if neg_counts:
                for p, c in neg_counts.items():
                    st.write(f"- `{p}` × {c}")
            else:
                st.write("_Không tìm thấy_")

        # Bước 2: Thống kê
        st.markdown("##### Bước 2 — Thống kê số lượng")
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        stat_col1.metric("Σ Tích cực (P)", pos_total)
        stat_col2.metric("Σ Tiêu cực (N)", neg_total)
        stat_col3.metric("Tổng cụm", total_phrases)

        # Bước 3: Tính score
        st.markdown("##### Bước 3 — Tính Sentiment Score")
        if total_phrases > 0:
            score = (pos_total - neg_total) / total_phrases
            st.latex(
                r"\text{Score} = \frac{P - N}{P + N} = "
                rf"\frac{{{pos_total} - {neg_total}}}{{{pos_total} + {neg_total}}} = "
                rf"{score:+.2f}"
            )
            st.caption("Score ∈ [−1, +1]. Gần +1 → tích cực, gần −1 → tiêu cực.")
        else:
            score = 0.0
            st.latex(r"\text{Score} = 0 \quad (\text{không phát hiện cụm nào})")

        # Bước 4: Quy tắc
        st.markdown("##### Bước 4 — Quy tắc phân loại")
        st.markdown(
            r"""
| Điều kiện | Nhãn |
|---|---|
| $P = 0$ và $N = 0$ | KHÔNG RÕ / TRUNG TÍNH |
| $P > N$ (Score > 0) | TÍCH CỰC |
| $N > P$ (Score < 0) | TIÊU CỰC |
| $P = N$ (Score = 0) | TRUNG TÍNH / LẪN LỘN |
"""
        )

        # Bước 5: Kết luận rule-based
        label = overall_sentiment(pos_total, neg_total)
        st.markdown("##### Bước 5 — Kết luận Rule-based")
        if "TÍCH CỰC" in label:
            st.success(f"➡️ P ({pos_total}) > N ({neg_total})  →  **{label}**  (Score = {score:+.2f})")
        elif "TIÊU CỰC" in label:
            st.error(f"➡️ N ({neg_total}) > P ({pos_total})  →  **{label}**  (Score = {score:+.2f})")
        else:
            st.warning(f"➡️ P ({pos_total}) = N ({neg_total})  →  **{label}**  (Score = {score:+.2f})")

        # --- Cách 2: underthesea sentiment ---
        st.markdown("---")
        st.markdown("#### 🤖 Cách 2 — underthesea `sentiment()`")

        # TODO 4b: Gọi safe_sentiment(text) và hiển thị kết quả.
        # ---- ĐÃ HOÀN THÀNH TODO 4b ----
        senti_label = safe_sentiment(text)
        senti_lower = senti_label.lower()

        if "positive" in senti_lower:
            st.success(f"**Nhãn underthesea:** `{senti_label}` 😊")
        elif "negative" in senti_lower:
            st.error(f"**Nhãn underthesea:** `{senti_label}` 😞")
        elif "lỗi" in senti_lower:
            st.warning(f"⚠️ {senti_label}")
        else:
            st.info(f"**Nhãn underthesea:** `{senti_label}` 😐")
        # --------------------------------

        # --- So sánh 2 cách ---
        st.markdown("---")
        st.markdown("#### 🔍 So sánh 2 phương pháp")

        # Ánh xạ nhãn underthesea → tiếng Việt để so sánh trực quan
        label_map = {
            "positive": "TÍCH CỰC",
            "negative": "TIÊU CỰC",
            "neutral":  "TRUNG TÍNH",
        }
        senti_vn = label_map.get(senti_lower.strip(), senti_label.upper())
        match_icon = "✅ Khớp nhau" if senti_vn == label else "⚠️ Khác nhau"

        st.markdown(
            f"""
| Tiêu chí | Rule-based | underthesea |
|---|---|---|
| Cách hoạt động | Đếm cụm từ trong danh sách cố định | Model NLP đã huấn luyện |
| Ưu điểm | Đơn giản, dễ hiểu, minh bạch | Chính xác hơn, xử lý ngữ cảnh |
| Nhược điểm | Bỏ sót nhiều, phụ thuộc danh sách | Cần cài model, khó giải thích |
| **Kết quả văn bản này** | **{label}** | **{senti_vn}** |
| **Nhận xét** | — | {match_icon} |
"""
        )

    else:
        st.info("Nhập văn bản và bấm **Phân tích** để bắt đầu demo.")
