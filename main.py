import streamlit as st
import pandas as pd

# ==========================================
# 1. 페이지 기본 설정 및 디자인 테마
# ==========================================
st.set_page_config(
    page_title="OTT-Finder | 오늘 뭐 볼까?", 
    layout="wide", 
    page_icon="🍿",
    initial_sidebar_state="expanded"
)

# 대시보드를 더 깔끔하게 만들기 위한 커스텀 CSS 스타일링
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #E50914; font-weight: 800; }
    .stMetric { background-color: #f0f2f6; padding: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 데이터 에셋 (실제 데이터로 확장 가능)
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
# 3. 사이드바 제어 패널 (입력창 디자인 고도화)
# ==========================================
with st.sidebar:
    st.title("🎬 시청 취향 필터")
    st.write("원하는 조건을 선택하면 실시간으로 분석 및 추천이 업데이트됩니다.")
    st.write("---")
    
    user_category = st.multiselect(
        "🗂️ 콘텐츠 종류", 
        options=['영화', '드라마', '예능'], 
        default=['영화', '드라마', '예능']
    )
    
    user_platform = st.multiselect(
        "📱 구독 중인 OTT 플랫폼", 
        options=['넷플릭스', '티빙', '디즈니+', '유튜브'], 
        default=['넷플릭스', '티빙', '디즈니+']
    )
    
    user_time = st.slider(
        "⏳ 최대 가용 시간 (분)", 
        min_value=30, max_value=200, value=150, step=10
    )
    
    user_age = st.checkbox("🔞 청소년 관람불가 콘텐츠 제외", value=False)

# ==========================================
# 4. 메인 대시보드 화면
# ==========================================
st.title("🍿 OTT-Finder")
st.subheader("남녀노소 취향 저격 통합 콘텐츠 추천 시스템")
st.write("---")

# 데이터 필터링 조건 적용
filtered_df = df.copy()
filtered_df = filtered_df[filtered_df['카테고리'].isin(user_category)]
filtered_df = filtered_df[filtered_df['플랫폼'].isin(user_platform)]
filtered_df = filtered_df[filtered_df['시간(분)'] <= user_time]

if user_age:
    filtered_df = filtered_df[filtered_df['연령제한'] != '청불']

# 레이아웃 분할 (왼쪽: 주요 시각화 및 지표, 오른쪽: 추천 결과 표)
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("### 📊 추천 데이터 요약")
    
    if filtered_df.empty:
        st.info("조건을 조정하시면 통계가 표시됩니다.")
    else:
        # 상단 핵심 지표(Metric) 카드 위젯 디자인
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric(label="🎯 추천 작품 수", value=f"{len(filtered_df)}개")
        with metric_col2:
            avg_rating = filtered_df['평점'].mean()
            st.metric(label="⭐ 평균 로튼 평점", value=f"{avg_rating:.1f}/100")
        
        st.write("")
        st.write("📌 **플랫폼별 콘텐츠 분포**")
        # 가독성이 좋은 수평 바 차트 활용
        platform_counts = filtered_df['플랫폼'].value_counts()
        st.bar_chart(platform_counts, horizontal=True, color="#E50914")

with col2:
    st.markdown("### ✨ 당신을 위한 맞춤형 콘텐츠")
    
    if filtered_df.empty:
        st.warning("🧐 선택하신 조건에 맞는 콘텐츠가 없습니다. 가용 시간을 늘리거나 플랫폼을 추가해 보세요!")
    else:
        # 평점 높은 순으로 정렬하여 유저에게 노출
        result_df = filtered_df.sort_values(by='평점', ascending=False)
        
        # 스트림릿 최신 전용 데이터프레임 위젯 (검색 및 정렬 기능 기본 내장)
        st.dataframe(
            result_df[['플랫폼', '카테고리', '제목', '장르', '시간(분)', '평점', '연령제한']],
            use_container_width=True,
            hide_index=True
        )
