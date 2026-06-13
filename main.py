import streamlit as st
import pandas as pd
import time

# ==========================================
# 1. 페이지 기본 설정 및 무조건 블루로 바꾸는 CSS
# ==========================================
st.set_page_config(
    page_title="OTT CONTENTS SELECTOR", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 스트림릿의 모든 요소를 샅샅이 뒤져서 블루로 강제 정복하는 CSS
st.markdown("""
    <style>
    /* 1. 전체 배경 및 텍스트 */
    .main { background-color: #0F172A; color: #F8FAFC; }
    .main .block-container { padding-top: 4rem; padding-bottom: 4rem; max-width: 950px; }
    
    /* 2. 타이틀 및 헤더 스타일 */
    h1 { color: #38BDF8; font-weight: 900; text-align: center; font-family: 'Inter', sans-serif; }
    h3 { color: #F8FAFC; font-weight: 700; margin-top: 2rem; border-left: 4px solid #38BDF8; padding-left: 10px; }
    .subtitle { text-align: center; color: #94A3B8; font-size: 1.1rem; margin-bottom: 3rem; }
    label, .stMultiSelect label, .stSlider label, .stCheckbox label { color: #E2E8F0 !important; font-weight: 600; }
    
    /* 3. [긴급 수리] 멀티셀렉트 내부 빨간 태그 무조건 파란색으로 덮어쓰기 */
    div[data-testid="stMultiSelectTag"] { 
        background-color: #0284C7 !important; /* 배경을 진한 블루로 */
        color: #FFFFFF !important;            /* 글자는 화이트 */
        border: none !important;
        border-radius: 4px !important;
    }
    div[data-testid="stMultiSelectTag"] span { color: #FFFFFF !important; }
    div[data-testid="stMultiSelectTag"] button { color: #FFFFFF !important; }
    
    /* 포커스 되었을 때 테두리 */
    div[data-baseweb="select"] > div { background-color: #1E293B !important; color: white !important; border-color: #334155 !important; }
    div[data-baseweb="select"] > div:focus-within { border-color: #38BDF8 !important; }

    /* 4. [긴급 수리] 슬라이더 빨간색 선과 붉은 숫자 완벽 차단 */
    /* 슬라이더 채워지는 바 */
    div[data-testid="stSliderTrack"] > div > div { background-color: #38BDF8 !important; }
    /* 슬라이더 둥근 손잡이 */
    div[role="slider"] { background-color: #38BDF8 !important; box-shadow: 0 0 10px rgba(56, 189, 248, 0.5) !important; }
    /* 슬라이더 위에 뜨는 빨간색 숫자 텍스트 제거 및 블루화 */
    div[data-testid="stSlider"] div { color: #38BDF8 !important; }
    
    /* 5. 체크박스 테두리 및 체크 색상 */
    div[data-testid="stCheckbox"] input[type="checkbox"]:checked + div { background-color: #38BDF8 !important; border-color: #38BDF8 !important; }

    /* 6. 메인 매칭 버튼 */
    .stButton>button { 
        width: 100%; 
        background-color: #0284C7; 
        color: white; 
        font-weight: 700; 
        font-size: 1.1rem;
        height: 3.5rem; 
        border-radius: 6px; 
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #0369A1; color: white; box-shadow: 0 0 15px rgba(56, 189, 248, 0.3); }
    
    /* 7. 통계 지표 박스 */
    div[data-testid="stMetric"] { background-color: #1E293B; border: 1px solid #334155; padding: 20px; border-radius: 8px; text-align: center; }
    div[data-testid="stMetricLabel"] { color: #94A3B8 !important; }
    div[data-testid="stMetricValue"] { color: #F8FAFC !important; font-weight: 800; }
    
    hr { border-color: #334155; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 데이터 에셋
# ==========================================
@st.cache_data
def load_data():
    data = {
        '제목': [
            '오징어 게임 시즌2', '괴물', '에밀리, 파리에 가다', 
            '인터스텔라', '라라랜드', '어벤져스: 엔드게임', 
            '솔로지옥', '스트릿 우먼 파이터', '무한도전 레전드'
        ],
        '카테고리': ['드라마', '영화', '드라마', '영화', '영화', '영화', '예능', '예능', '예능'],
        '장르': ['스릴러/서바이벌', '스릴러/범죄', '로맨스/코미디', 'SF/액션', '로맨스/뮤지컬', 'SF/액션', '로맨스/리얼리티', '댄스/경연', '코미디/토크'],
        '플랫폼': ['넷플릭스', '티빙', '넷플릭스', '디즈니+', '넷플릭스', '디즈니+', '넷플릭스', '티빙', '유튜브'],
        '시간(분)': [50, 120, 30, 169, 128, 181, 60, 90, 45],
        '평점': [92, 88, 75, 74, 91, 94, 80, 85, 98],
        '연령제한': ['청불', '15세', '15세', '12세', '12세', '12세', '15세', '15세', '12세']
    }
    return pd.DataFrame(data)

df = load_data()

# ==========================================
# 3. 메인 화면 타이틀
# ==========================================
st.title("OTT CONTENTS SELECTOR")
st.markdown("<p class='subtitle'>사용자 맞춤형 콘텐츠 분석 및 추천 알고리즘 시스템</p>", unsafe_allow_html=True)
st.write("---")

if 'search_clicked' not in st.session_state:
    st.session_state.search_clicked = False

def trigger_search():
    st.session_state.search_clicked = True

# ==========================================
# 4. [1단계] 조건 설정 섹션
# ==========================================
st.markdown("### 01. 선호 시청 환경 설정")

with st.container():
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        user_category = st.multiselect(
            "콘텐츠 유형", 
            options=['영화', '드라마', '예능'], 
            default=['영화', '드라마']
        )
        user_platform = st.multiselect(
            "보유 중인 플랫폼 디바이스", 
            options=['넷플릭스', '티빙', '디즈니+', '유튜브'], 
            default=['넷플릭스', '티빙']
        )
        
    with col2:
        user_time = st.slider(
            "최대 가용 시간 (분 단위)", 
            min_value=30, max_value=200, value=130, step=10
        )
        user_age = st.checkbox("청소년 관람불가 등급 제외", value=False)

st.write("")
st.button("MATCHING CONTENT", on_click=trigger_search)
st.write("---")

# ==========================================
# 5. [2단계] 결과 분석 및 추천 테이블
# ==========================================
if st.session_state.search_clicked:
    
    filtered_df = df.copy()
    filtered_df = filtered_df[filtered_df['카테고리'].isin(user_category)]
    filtered_df = filtered_df[filtered_df['플랫폼'].isin(user_platform)]
    filtered_df = filtered_df[filtered_df['시간(분)'] <= user_time]
    if user_age:
        filtered_df = filtered_df[filtered_df['연령제한'] != '청불']

    with st.spinner('데이터베이스 쿼리 분석 중...'):
        time.sleep(0.8)
        
    st.markdown("### 02. 알고리즘 매칭 결과 및 데이터 분석")
    
    if filtered_df.empty:
        st.error("설정하신 조건과 일치하는 콘텐츠 정보가 존재하지 않습니다. 조건을 재설정해 주십시오.")
    else:
        result_df = filtered_df.sort_values(by='평점', ascending=False)
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric(label="매칭된 총 작품 수", value=f"{len(filtered_df)} UNIT")
        with metric_col2:
            st.metric(label="추천 집합 평균 평점", value=f"{filtered_df['평점'].mean():.1f} / 100")
        with metric_col3:
            st.metric(label="최적 매칭 플랫폼", value=f"{filtered_df['플랫폼'].mode()[0]}")
            
        st.write("")
        
        st.dataframe(
            result_df[['플랫폼', '카테고리', '제목', '장르', '시간(분)', '평점', '연령제한']],
            use_container_width=True,
            hide_index=True
        )
        
        st.write("")
        st.write("▼ **플랫폼별 추천 비중 통계**")
        st.bar_chart(filtered_df['플랫폼'].value_counts(), color="#38BDF8")
