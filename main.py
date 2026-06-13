import streamlit as st
import pandas as pd
import time

# ==========================================
# 1. 페이지 기본 설정 및 시네마 다크 테마 CSS
# ==========================================
st.set_page_config(
    page_title="OTT CONTENTS SELECTOR", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 영화관 무드를 내기 위한 커스텀 다크 CSS 스타일링
st.markdown("""
    <style>
    /* 전체 배경 및 텍스트 색상 제어 */
    .main { background-color: #141414; color: #FFFFFF; }
    .main .block-container { padding-top: 4rem; padding-bottom: 4rem; max-width: 950px; }
    
    /* 타이틀 및 폰트 스타일 */
    h1 { color: #E50914; font-weight: 900; letter-spacing: -1px; text-align: center; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    h3 { color: #FFFFFF; font-weight: 700; margin-top: 2rem; border-left: 4px solid #E50914; padding-left: 10px; }
    .subtitle { text-align: center; color: #A3A3A3; font-size: 1.1rem; margin-bottom: 3rem; }
    
    /* 입력창 및 라벨 색상 조정 */
    label, .stMultiSelect label, .stSlider label, .stCheckbox label { color: #E5E5E5 !important; font-weight: 600; }
    
    /* 대형 버튼 스타일 (영화관 매표소 느낌) */
    .stButton>button { 
        width: 100%; 
        background-color: #E50914; 
        color: white; 
        font-weight: 700; 
        font-size: 1.1rem;
        height: 3.5rem; 
        border-radius: 4px; 
        border: none;
        letter-spacing: 1px;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #B81D24; color: white; box-shadow: 0 0 15px rgba(229, 9, 20, 0.4); }
    
    /* 통계 지표 박스 */
    div[data-testid="stMetric"] { 
        background-color: #1F1F1F; 
        border: 1px solid #2F2F2F; 
        padding: 20px; 
        border-radius: 6px; 
        text-align: center;
    }
    div[data-testid="stMetricLabel"] { color: #A3A3A3 !important; }
    div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 800; }
    
    /* 구분선 */
    hr { border-color: #2F2F2F; }
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
st.title("CINEMA OTT INDEX")
st.markdown("<p class='subtitle'>사용자 맞춤형 콘텐츠 분석 및 추천 알고리즘 시스템</p>", unsafe_allow_html=True)
st.write("---")

# 세션 상태 초기화
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
    
    # 필터링 조건 연산
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
        # 평점순 정렬
        result_df = filtered_df.sort_values(by='평점', ascending=False)
        
        # 핵심 메트릭 지표
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric(label="매칭된 총 작품 수", value=f"{len(filtered_df)} UNIT")
        with metric_col2:
            st.metric(label="추천 집합 평균 평점", value=f"{filtered_df['평점'].mean():.1f} / 100")
        with metric_col3:
            st.metric(label="최적 매칭 플랫폼", value=f"{filtered_df['플랫폼'].mode()[0]}")
            
        st.write("")
        
        # 데이터프레임 노출 (어두운 테마에 맞춰 스트림릿이 자동 최적화)
        st.dataframe(
            result_df[['플랫폼', '카테고리', '제목', '장르', '시간(분)', '평점', '연령제한']],
            use_container_width=True,
            hide_index=True
        )
        
        # 하단 통계 그래프 (시네마 레드 단색 차트)
        st.write("")
        st.write("▼ **플랫폼별 추천 비중 통계**")
        st.bar_chart(filtered_df['플랫폼'].value_counts(), color="#E50914")
