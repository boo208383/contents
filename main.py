import streamlit as st
import pandas as pd
import time

# ==========================================
# 1. 페이지 기본 설정 및 디자인 테마
# ==========================================
st.set_page_config(
    page_title="OTT-Finder | 취향 매칭", 
    layout="wide", 
    page_icon="🍿"
)

# 깔끔하고 모던한 UI를 위한 CSS
st.markdown("""
    <style>
    .main .block-container { padding-top: 3rem; padding-bottom: 3rem; max-width: 1000px; }
    h1 { color: #E50914; font-weight: 800; text-align: center; }
    .subtitle { text-align: center; color: #666; margin-bottom: 2rem; }
    .stButton>button { width: 100%; background-color: #E50914; color: white; font-weight: bold; height: 3rem; border-radius: 8px; border: none; }
    .stButton>button:hover { background-color: #b80710; color: white; }
    .box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
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
st.title("🎬 OTT-Finder")
st.markdown("<p class='subtitle'>당신의 취향을 분석하여 딱 맞는 콘텐츠를 찾아드립니다.</p>", unsafe_allow_html=True)
st.write("---")

# Session State(상태 유지)를 활용해 버튼 클릭 여부 추적
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

# ==========================================
# 4. [1단계] 취향 선택 창 (처음에만 집중해서 보이도록)
# ==========================================
st.markdown("### 🍿 Step 1. 오늘의 시청 스타일 선택")

# 깔끔하게 구획을 나누기 위한 컨테이너
with st.container():
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        user_category = st.multiselect(
            "🗂️ 보고 싶은 콘텐츠 종류", 
            options=['영화', '드라마', '예능'], 
            default=['영화', '드라마']
        )
        user_platform = st.multiselect(
            "📱 구독 중인 OTT 플랫폼", 
            options=['넷플릭스', '티빙', '디즈니+', '유튜브'], 
            default=['넷플릭스', '티빙']
        )
        
    with col2:
        user_time = st.slider(
            "⏳ 오늘 쓸 수 있는 시간 (최대 몇 분?)", 
            min_value=30, max_value=200, value=120, step=10
        )
        user_age = st.checkbox("🔞 청소년 관람불가 콘텐츠는 제외할래요", value=False)

st.write("")
# 추천 받기 버튼 (누르면 click_button 함수 실행)
st.button("✨ 내 취향에 맞는 콘텐츠 추천받기", on_click=click_button)
st.write("---")

# ==========================================
# 5. [2단계] 결과 출력 창 (버튼을 누른 후에만 등장!)
# ==========================================
if st.session_state.clicked:
    
    # 데이터 필터링 조건 적용
    filtered_df = df.copy()
    filtered_df = filtered_df[filtered_df['카테고리'].isin(user_category)]
    filtered_df = filtered_df[filtered_df['플랫폼'].isin(user_platform)]
    filtered_df = filtered_df[filtered_df['시간(분)'] <= user_time]
    if user_age:
        filtered_df = filtered_df[filtered_df['연령제한'] != '청불']

    # 애니메이션 효과처럼 보이도록 분석 중 메세지 띄우기 (발표용 꿀팁)
    with st.spinner('🎯 당신의 시청 취향 데이터를 분석하는 중입니다...'):
        time.sleep(1) # 1초 대기 효과
        
    st.markdown("### 📊 Step 2. 취향 분석 및 추천 결과")
    
    if filtered_df.empty:
        st.error("🧐 선택하신 조건에 맞는 콘텐츠가 데이터베이스에 없습니다. 가용 시간을 늘리거나 플랫폼을 추가해 보세요!")
    else:
        # 평점 높은 순 정렬
        result_df = filtered_df.sort_values(by='평점', ascending=False)
        
        # 지표 카드 시각화
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric(label="🎯 매칭된 작품 수", value=f"{len(filtered_df)}개")
        with metric_col2:
            st.metric(label="⭐ 추천 카테고리 평균 평점", value=f"{filtered_df['평점'].mean():.1f}/100")
        with metric_col3:
            st.metric(label="🎬 가장 많이 추천된 플랫폼", value=f"{filtered_df['플랫폼'].mode()[0]}")
            
        st.write("")
        
        # 추천 리스트 표 출력
        st.dataframe(
            result_df[['플랫폼', '카테고리', '제목', '장르', '시간(분)', '평점', '연령제한']],
            use_container_width=True,
            hide_index=True
        )
        
        # 하단 미니 차트
        st.write("")
        st.write("📌 **추천 콘텐츠의 플랫폼별 비중**")
        st.bar_chart(filtered_df['플랫폼'].value_counts(), color="#E50914")
