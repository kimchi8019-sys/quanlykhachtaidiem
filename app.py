import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

st.set_page_config(
    page_title="Tourism Crowd Manager",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# STYLE
# =========================
st.markdown("""
<style>
    .stApp {
        background: #f5f7fb;
    }
    .hero {
        padding: 28px 34px;
        border-radius: 18px;
        margin-bottom: 22px;
        background:
            linear-gradient(90deg, rgba(0,70,80,.88), rgba(0,70,80,.35)),
            url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1800&q=85");
        background-size: cover;
        background-position: center;
        color: white;
        min-height: 190px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .hero h1 {
        font-size: 38px;
        margin: 0;
        font-weight: 800;
    }
    .hero p {
        font-size: 17px;
        margin-top: 8px;
        opacity: .95;
    }
    .metric-card {
        background: white;
        padding: 18px 20px;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,.06);
        border: 1px solid #edf0f5;
    }
    .metric-title {
        color: #687386;
        font-size: 14px;
    }
    .metric-value {
        font-size: 30px;
        font-weight: 800;
        color: #183b56;
        margin-top: 4px;
    }
    .metric-note {
        color: #758195;
        font-size: 12px;
    }
    .section-title {
        font-size: 22px;
        font-weight: 750;
        color: #183b56;
        margin: 22px 0 12px 0;
    }
    .status-ok {
        background: #e8f7ef;
        color: #18794e;
        padding: 6px 10px;
        border-radius: 999px;
        font-weight: 700;
    }
    .status-warning {
        background: #fff5d9;
        color: #9a6700;
        padding: 6px 10px;
        border-radius: 999px;
        font-weight: 700;
    }
    .status-danger {
        background: #fdeaea;
        color: #b42318;
        padding: 6px 10px;
        border-radius: 999px;
        font-weight: 700;
    }
    div[data-testid="stSidebar"] {
        background: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION DATA
# =========================
if "destinations" not in st.session_state:
    st.session_state.destinations = pd.DataFrame([
        {"id": "D01", "Điểm đến": "Bạch Dinh", "Địa điểm": "Vũng Tàu", "Sức chứa": 300, "Khách hiện tại": 86},
        {"id": "D02", "Điểm đến": "Hồ Mây", "Địa điểm": "Vũng Tàu", "Sức chứa": 500, "Khách hiện tại": 214},
        {"id": "D03", "Điểm đến": "Địa đạo Long Phước", "Địa điểm": "Bà Rịa", "Sức chứa": 180, "Khách hiện tại": 72},
        {"id": "D04", "Điểm đến": "Minh Đạm", "Địa điểm": "Long Điền", "Sức chứa": 250, "Khách hiện tại": 119},
        {"id": "D05", "Điểm đến": "Côn Đảo", "Địa điểm": "Côn Đảo", "Sức chứa": 800, "Khách hiện tại": 421},
    ])

if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame([
        {
            "Mã": "LOG001",
            "Thời gian": "2026-09-29 08:15",
            "Điểm đến": "Bạch Dinh",
            "Loại": "Khách vào",
            "Số lượng": 35,
            "Ghi chú": "Đoàn khách Hà Nội"
        },
        {
            "Mã": "LOG002",
            "Thời gian": "2026-09-29 09:05",
            "Điểm đến": "Hồ Mây",
            "Loại": "Khách vào",
            "Số lượng": 60,
            "Ghi chú": "Khách lẻ"
        },
    ])

# =========================
# FUNCTIONS
# =========================
def status_info(current, capacity):
    ratio = current / capacity if capacity else 0
    if ratio >= 1:
        return "QUÁ TẢI", "danger"
    if ratio >= 0.8:
        return "GẦN ĐẦY", "warning"
    return "BÌNH THƯỜNG", "ok"

def add_history(destination, action, quantity, note):
    new_row = pd.DataFrame([{
        "Mã": "LOG" + uuid.uuid4().hex[:7].upper(),
        "Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Điểm đến": destination,
        "Loại": action,
        "Số lượng": quantity,
        "Ghi chú": note or ""
    }])
    st.session_state.history = pd.concat(
        [new_row, st.session_state.history],
        ignore_index=True
    )

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.image(
        "https://images.unsplash.com/photo-1526772662000-3f88f10405ff?auto=format&fit=crop&w=800&q=80",
        use_container_width=True
    )
    st.markdown("### 🌴 Tourism Crowd Manager")
    st.caption("Quản lý lượng khách tại điểm đến")

    menu = st.radio(
        "CHỨC NĂNG",
        ["📊 Tổng quan", "👥 Cập nhật du khách", "🗺️ Quản lý điểm đến", "📋 Lịch sử"]
    )

    st.divider()
    st.caption("Hệ thống quản lý điểm đến")
    st.caption("© 2026 Tourism Manager")

# =========================
# HEADER
# =========================
st.markdown("""
<div class="hero">
    <h1>🌴 QUẢN LÝ DU KHÁCH TẠI ĐIỂM ĐẾN</h1>
    <p>Theo dõi số lượng khách theo thời gian thực • Kiểm soát sức chứa • Hỗ trợ điều hành du lịch</p>
</div>
""", unsafe_allow_html=True)

dest = st.session_state.destinations.copy()
total_capacity = int(dest["Sức chứa"].sum())
total_current = int(dest["Khách hiện tại"].sum())
destination_count = len(dest)
busy_count = int((dest["Khách hiện tại"] / dest["Sức chứa"] >= 0.8).sum())
usage = total_current / total_capacity * 100 if total_capacity else 0

# =========================
# DASHBOARD
# =========================
if menu == "📊 Tổng quan":
    c1, c2, c3, c4 = st.columns(4)

    cards = [
        ("👥", "TỔNG DU KHÁCH", f"{total_current:,}", "Khách đang có mặt"),
        ("🗺️", "ĐIỂM ĐẾN", f"{destination_count}", "Điểm đang quản lý"),
        ("📈", "CÔNG SUẤT", f"{usage:.1f}%", "So với tổng sức chứa"),
        ("🚦", "CẦN THEO DÕI", f"{busy_count}", "Điểm đạt từ 80% công suất"),
    ]

    for col, (icon, title, value, note) in zip([c1,c2,c3,c4], cards):
        with col:
            st.markdown(
                f"""<div class="metric-card">
                    <div class="metric-title">{icon} {title}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-note">{note}</div>
                </div>""",
                unsafe_allow_html=True
            )

    st.markdown('<div class="section-title">📍 Tình trạng từng điểm đến</div>', unsafe_allow_html=True)

    display = dest.copy()
    display["Công suất"] = (
        display["Khách hiện tại"] / display["Sức chứa"] * 100
    ).round(1)

    def progress_text(x):
        if x >= 100:
            return "🔴 QUÁ TẢI"
        if x >= 80:
            return "🟡 GẦN ĐẦY"
        return "🟢 BÌNH THƯỜNG"

    display["Trạng thái"] = display["Công suất"].apply(progress_text)

    st.dataframe(
        display[[
            "Điểm đến", "Địa điểm", "Khách hiện tại",
            "Sức chứa", "Công suất", "Trạng thái"
        ]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Công suất": st.column_config.ProgressColumn(
                "Công suất",
                min_value=0,
                max_value=100,
                format="%.1f%%"
            )
        }
    )

    st.markdown('<div class="section-title">📊 Phân bố du khách</div>', unsafe_allow_html=True)
    chart_data = dest.set_index("Điểm đến")[["Khách hiện tại", "Sức chứa"]]
    st.bar_chart(chart_data, use_container_width=True)

# =========================
# UPDATE TOURISTS
# =========================
elif menu == "👥 Cập nhật du khách":
    st.markdown('<div class="section-title">👥 Cập nhật số lượng du khách</div>', unsafe_allow_html=True)

    selected = st.selectbox("Chọn điểm đến", dest["Điểm đến"].tolist())
    row_index = dest.index[dest["Điểm đến"] == selected][0]
    current = int(dest.loc[row_index, "Khách hiện tại"])
    capacity = int(dest.loc[row_index, "Sức chứa"])

    a, b, c = st.columns(3)
    a.metric("Khách hiện tại", f"{current:,}")
    b.metric("Sức chứa", f"{capacity:,}")
    c.metric("Còn có thể tiếp nhận", f"{max(capacity-current,0):,}")

    st.divider()

    action = st.radio(
        "Loại cập nhật",
        ["➕ Khách vào", "➖ Khách rời điểm đến"],
        horizontal=True
    )

    with st.form("visitor_form"):
        quantity = st.number_input(
            "Số lượng du khách",
            min_value=1,
            max_value=10000,
            value=1,
            step=1
        )
        note = st.text_input(
            "Ghi chú",
            placeholder="Ví dụ: Đoàn khách Hà Nội, khách đoàn 30 người..."
        )
        submitted = st.form_submit_button(
            "💾 CẬP NHẬT",
            use_container_width=True,
            type="primary"
        )

        if submitted:
            if "Khách vào" in action:
                new_value = current + quantity
                if new_value > capacity:
                    st.error(
                        f"⚠️ Không thể cập nhật. Số khách sẽ là {new_value:,}, "
                        f"vượt sức chứa {capacity:,}."
                    )
                else:
                    st.session_state.destinations.loc[row_index, "Khách hiện tại"] = new_value
                    add_history(selected, "Khách vào", quantity, note)
                    st.success(f"Đã ghi nhận {quantity:,} khách vào {selected}.")
                    st.rerun()
            else:
                new_value = current - quantity
                if new_value < 0:
                    st.error("⚠️ Số khách rời không thể lớn hơn số khách hiện tại.")
                else:
                    st.session_state.destinations.loc[row_index, "Khách hiện tại"] = new_value
                    add_history(selected, "Khách rời", quantity, note)
                    st.success(f"Đã ghi nhận {quantity:,} khách rời {selected}.")
                    st.rerun()

# =========================
# DESTINATIONS
# =========================
elif menu == "🗺️ Quản lý điểm đến":
    st.markdown('<div class="section-title">🗺️ Danh sách điểm đến</div>', unsafe_allow_html=True)

    st.dataframe(
        dest[["id", "Điểm đến", "Địa điểm", "Sức chứa", "Khách hiện tại"]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### ➕ Thêm điểm đến")

    with st.form("add_destination"):
        col1, col2 = st.columns(2)
        name = col1.text_input("Tên điểm đến")
        location = col2.text_input("Khu vực / địa phương")

        col3, col4 = st.columns(2)
        capacity = col3.number_input("Sức chứa tối đa", min_value=1, value=100, step=10)
        initial = col4.number_input("Số khách hiện tại", min_value=0, value=0, step=1)

        add = st.form_submit_button(
            "➕ THÊM ĐIỂM ĐẾN",
            use_container_width=True,
            type="primary"
        )

        if add:
            if not name.strip():
                st.error("Vui lòng nhập tên điểm đến.")
            elif name.strip() in st.session_state.destinations["Điểm đến"].values:
                st.error("Điểm đến này đã tồn tại.")
            elif initial > capacity:
                st.error("Số khách hiện tại không được lớn hơn sức chứa.")
            else:
                new_destination = pd.DataFrame([{
                    "id": "D" + uuid.uuid4().hex[:4].upper(),
                    "Điểm đến": name.strip(),
                    "Địa điểm": location.strip(),
                    "Sức chứa": capacity,
                    "Khách hiện tại": initial
                }])
                st.session_state.destinations = pd.concat(
                    [st.session_state.destinations, new_destination],
                    ignore_index=True
                )
                st.success(f"Đã thêm điểm đến: {name.strip()}")
                st.rerun()

# =========================
# HISTORY
# =========================
elif menu == "📋 Lịch sử":
    st.markdown('<div class="section-title">📋 Lịch sử cập nhật du khách</div>', unsafe_allow_html=True)

    history = st.session_state.history.copy()

    if not history.empty:
        f1, f2 = st.columns(2)
        destination_filter = f1.selectbox(
            "Lọc điểm đến",
            ["Tất cả"] + sorted(history["Điểm đến"].unique().tolist())
        )
        type_filter = f2.selectbox(
            "Lọc loại cập nhật",
            ["Tất cả", "Khách vào", "Khách rời"]
        )

        filtered = history.copy()

        if destination_filter != "Tất cả":
            filtered = filtered[filtered["Điểm đến"] == destination_filter]

        if type_filter != "Tất cả":
            filtered = filtered[filtered["Loại"] == type_filter]

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Tải lịch sử CSV",
            filtered.to_csv(index=False).encode("utf-8-sig"),
            "lich_su_du_khach.csv",
            "text/csv",
            use_container_width=True
        )
    else:
        st.info("Chưa có dữ liệu lịch sử.")

st.divider()
st.caption(
    f"🕒 Cập nhật giao diện: {datetime.now().strftime('%d/%m/%Y %H:%M')} "
    " • Hệ thống quản lý số lượng du khách tại điểm đến"
)

