import streamlit as st
import pandas as pd
import time

# ==========================================
# 1. 페이지 기본 설정 및 레이아웃
# ==========================================
st.set_page_config(
    page_title="OTT CONTENTS SELECTOR", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# UI 스타일을 깔끔하게 다듬는 CSS
st.markdown("""
    <style>
    .main .block-container { padding-top: 3rem; padding-bottom: 4rem; max-width: 1050px; }
    h1 { font-weight: 900; text-align: center; font-family: 'Inter', sans-serif; margin-bottom: 0.5rem; }
    h3 { font-weight: 700; margin-top: 2.5rem; border-left: 4px solid #38BDF8; padding-left: 12px; }
    .subtitle { text-align: center; color: #94A3B8; font-size: 1.1rem; margin-bottom: 3rem; }
    
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
    .stButton>button:hover { background-color: #0369A1; box-shadow: 0 0 15px rgba(56, 189, 248, 0.3); }
    
    div[data-testid="stMetric"] { padding: 20px; border-radius: 8px; text-align: center; }
    hr { border-color: #334155; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 방대한 45개 리얼 트렌드 데이터셋 (대표 장르 그룹 추가)
# ==========================================
@st.cache_data
def load_massive_data():
    data = {
        '제목': [
            # 영화 (15개)
            '파묘', '서울의 봄', '범죄도시4', '인사이드 아웃 2', '듄: 파트2',
            '오펜하이머', '엘리멘탈', '스파이더맨: 어크로스 더 유니버스', '탑건: 매버릭', '아바타: 물의 길',
            '인터스텔라', '라라랜드', '기생충', '올드보이', '헤어질 결심',
            # 드라마 (15개)
            '오징어 게임 시즌2', '선재 업고 튀어', '눈물의 여왕', '더 글로리', '무빙',
            '비밀의 숲', '지옥 시즌2', '무인도의 디바', '정년이', '지배종',
            '삼시세끼 Light', '괴물', '킹덤', '이태원 클라쓰', '응답하라 1988',
            # 예능 (15개)
            '흑백요리사: 요리 계급 전쟁', '신서유기 레전드', '무한도전 명작선', '피지컬: 100', '환승연애 시즌3',
            '나 혼자 산다', '런닝맨', '최강야구', '유 퀴즈 온 더 블럭', '태어난 김에 세계일주',
            '아는 형님', '나는 SOLO', '크라임씬 리턴즈', '대탈출', '꼬리에 꼬리를 무는 그날 이야기'
        ],
        '카테고리': [
            '영화', '영화', '영화', '영화', '영화', '영화', '영화', '영화', '영화', '영화', '영화', '영화', '영화', '영화', '영화',
            '드라마', '드라마', '드라마', '드라마', '드라마', '드라마', '드라마', '드라마', '드라마', '드라마', '드라마', '드라마', '드라마', '드라마', '드라마',
            '예능', '예능', '예능', '예능', '예능', '예능', '예능', '예능', '예능', '예능', '예능', '예능', '예능', '예능', '예능'
        ],
        # 사용자가 고를 5대 대표 장르 맵핑
        '장르그룹': [
            '스릴러/공포', '드라마/로맨스', '액션/SF', '코미디/토크', '액션/SF',
            '스릴러/공포', '드라마/로맨스', '액션/SF', '액션/SF', '액션/SF',
            '액션/SF', '드라마/로맨스', '스릴러/공포', '스릴러/공포', '드라마/로맨스',
            '스릴러/공포', '드라마/로맨스', '드라마/로맨스', '스릴러/공포', '액션/SF',
            '스릴러/공포', '액션/SF', '드라마/로맨스', '드라마/로맨스', '액션/SF',
            '예능/리얼리티', '스릴러/공포', '스릴러/공포', '드라마/로맨스', '드라마/로맨스',
            '예능/리얼리티', '코미디/토크', '코미디/토크', '예능/리얼리티', '예능/리얼리티',
            '예능/리얼리티', '코미디/토크', '예능/리얼리티', '코미디/토크', '예능/리얼리티',
            '코미디/토크', '예능/리얼리티', '스릴러/공포', '스릴러/공포', '예능/리얼리티'
        ],
        '세부장르': [
            '오컬트/스릴러', '역사/드라마', '액션/범죄', '애니메이션/코미디', 'SF/판타지',
            '스릴러/드라마', '애니메이션/로맨스', '애니메이션/액션', '액션/드라마', 'SF/판타지',
            'SF/액션', '로맨스/뮤지컬', '스릴러/드라마', '스릴러/범죄', '로맨스/미스터리',
            '스릴러/서바이벌', '로맨스/판타지', '로맨스/드라마', '스릴러/범죄', 'SF/액션',
            '스릴러/범죄', 'SF/스릴러', '로맨스/드라마', '음악/드라마', 'SF/스릴러',
            '리얼리티/예능', '스릴러/범죄', '스릴러/좀비', '청춘/드라마', '가족/드라마',
            '요리/경연', '코미디/토크', '코미디/토크', '스포츠/서바이벌', '로맨스/리얼리티',
            '리얼리티/예능', '코미디/토크', '스포츠/예능', '코미디/토크', '여행/리얼리티',
            '코미디/토크', '로맨스/리얼리티', '추리/게임', '추리/게임', '시사/교양'
        ],
        '플랫폼': [
            '티빙', '웨이브', '디즈니+', '디즈니+', '웨이브',
            '넷플릭스', '디즈니+', '디즈니+', '넷플릭스', '디즈니+',
            '넷플릭스', '왓챠', '넷플릭스', '왓챠', '티빙',
            '넷플릭스', '티빙', '티빙', '넷플릭스', '디즈니+',
            '티빙', '넷플릭스', 'tvN', '디즈니+', '디즈니+',
            '유튜브', '티빙', '넷플릭스', '넷플릭스', '티빙',
            '넷플릭스', '티빙', '유튜브', '넷플릭스', '티빙',
            '웨이브', 'SBS', '넷플릭스', '티빙', '웨이브',
            'JTBC', 'SBS', '티빙', '티빙', '유튜브'
        ],
        '시간(분)': [
            134, 141, 109, 96, 166, 180, 101, 140, 130, 192, 169, 128, 132, 120, 138,
            55, 60, 80, 50, 45, 65, 50, 70, 60, 50, 80, 70, 50, 65, 90,
            100, 40, 45, 90, 120, 85, 80, 140, 95, 85, 90, 80, 110, 100, 50
        ],
        '평점': [
            86, 95, 78, 92, 93, 94, 88, 96, 97, 82, 74, 91, 99, 94, 89,
            92, 94, 89, 96, 93, 95, 72, 85, 91, 76, 88, 88, 94, 87, 92,
            95, 98, 99, 84, 80, 76, 82, 92, 89, 94, 73, 70, 91, 93, 87
        ],
        '연령제한': [
            '15세', '12세', '15세', '전체', '12세', '15세', '전체', '전체', '12세', '12세', '12세', '12세', '15세', '청불', '15세',
            '청불', '15세', '15세', '청불', '15세', '15세', '15세', '15세', '15세', '15세', '12세', '15세', '청불', '15세', '15세',
            '12세', '15세', '12세', '12세', '15세', '15세', '12세', '12세', '12세', '12세', '15세', '15세', '15세', '15세', '12세'
        ]
    }
    return pd.DataFrame(data)

df = load_massive_data()
genre_groups = ['드라마/로맨스', '액션/SF', '스릴러/공포', '예능/리얼리티', '코미디/토크']

# ==========================================
# 3. 메인 화면 타이틀
# ==========================================
st.title("OTT CONTENTS SELECTOR")
st.markdown("<p class='subtitle'>핵심 5대 장르 그룹 및 45개 트렌드 데이터를 기반으로 한 추천 알고리즘</p>", unsafe_allow_html=True)
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
            default=['영화', '드라마', '예능']
        )
        user_platform = st.multiselect(
            "보유 중인 플랫폼 디바이스", 
            options=['넷플릭스', '티빙', '디즈니+', '웨이브', '왓챠', '유튜브'], 
            default=['넷플릭스', '티빙', '유튜브']
        )
        # 깔끔하게 정리된 5가지 그룹만 선택지로 제공
        user_genre_group = st.multiselect(
            "선호 장르 대분류 (미선택 시 전체 장르 대상)",
            options=genre_groups,
            default=[]
        )
        
    with col2:
        user_time = st.slider(
            "최대 가용 시간 (분 단위)", 
            min_value=30, max_value=200, value=150, step=10
        )
        user_age = st.checkbox("청소년 관람불가 등급 제외", value=False)

st.write("")
st.button("MATCHING CONTENT", on_click=trigger_search)
st.write("---")

# ==========================================
# 5. [2단계] 결과 분석 및 추천 테이블
# ==========================================
if st.session_state.search_clicked:
    
    # 기본 필터링 연산
    filtered_df = df.copy()
    filtered_df = filtered_df[filtered_df['카테고리'].isin(user_category)]
    filtered_df = filtered_df[filtered_df['플랫폼'].isin(user_platform)]
    filtered_df = filtered_df[filtered_df['시간(분)'] <= user_time]
    
    # 깔끔해진 대분류 장르 필터링
    if user_genre_group:
        filtered_df = filtered_df[filtered_df['장르그룹'].isin(user_genre_group)]
        
    if user_age:
        filtered_df = filtered_df[filtered_df['연령제한'] != '청불']

    with st.spinner('대용량 콘텐츠 데이터베이스 쿼리 연산 중...'):
        time.sleep(1.0)
        
    st.markdown("### 02. 알고리즘 매칭 결과 및 데이터 분석")
    
    if filtered_df.empty:
        st.error("설정하신 조건과 일치하는 콘텐츠 정보가 존재하지 않습니다. 필터 범위를 넓혀 주십시오.")
    else:
        result_df = filtered_df.sort_values(by='평점', ascending=False)
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric(label="매칭된 총 작품 수", value=f"{len(filtered_df)} UNIT")
        with metric_col2:
            st.metric(label="추천 집합 평균 평점", value=f"{filtered_df['평점'].mean():.1f} / 100")
        with metric_col3:
            st.metric(label="최적 매칭 플랫폼", value=f"{filtered_df['플랫폼'].mode()[0] if not filtered_df['플랫폼'].empty else 'N/A'}")
            
        st.write("")
        
        # 표에는 사용자가 고른 '장르그룹' 대신 원래 디테일한 '세부장르'가 나오도록 출력하여 전문성 유지
        st.dataframe(
            result_df[['플랫폼', '카테고리', '제목', '세부장르', '시간(분)', '평점', '연령제한']],
            use_container_width=True,
            hide_index=True
        )
        
        st.write("")
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.write("▼ **플랫폼별 추천 점유율**")
            st.bar_chart(filtered_df['플랫폼'].value_counts())
            
        with chart_col2:
            st.write("▼ **추천 작품들의 장르별 평균 평점 분포**")
            genre_stats = filtered_df.groupby('장르그룹')['평점'].mean().sort_values(ascending=False)
            st.line_chart(genre_stats)
