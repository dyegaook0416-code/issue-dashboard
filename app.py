%%writefile app.py
import streamlit as st
import requests
import datetime
from urllib.parse import quote

# 1. 페이지 설정
st.set_page_config(page_title="실시간 이슈 대시보드", layout="wide")

# 2. 디자인 설정 (표를 없애고 버튼 가시성 강화)
st.markdown("""
    <style>
    .stApp { background-color: #FFD700; color: #000000; }
    .top-bar { background-color: #0047AB; height: 6px; width: 100%; position: fixed; top: 0; left: 0; z-index: 9999; }
    .main-title { font-size: 2.8em; font-weight: 900; color: #000000; text-align: center; margin-top: 40px; }
    .update-time { font-size: 0.9em; color: #333333; text-align: center; margin-bottom: 30px; font-weight: 600; }

    /* 섹션 제목 스타일 */
    .section-header { 
        font-size: 1.5em; 
        font-weight: 800; 
        color: #0047AB; 
        text-align: center; 
        margin: 30px 0 15px 0; 
        padding-bottom: 10px;
        border-bottom: 3px solid #000000;
    }

    /* 버튼 공통 스타일 */
    .search-btn {
        width: 100%;
        height: 50px;
        background-color: #FFFFFF;
        color: #000000;
        border: 2px solid #000000;
        border-radius: 12px;
        font-size: 1.1em;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-bottom: 10px;
        box-shadow: 4px 4px 0px #0047AB;
    }
    .search-btn:hover {
        background-color: #0047AB;
        color: #FFFFFF;
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px #000000;
    }
    
    /* 카테고리용 작은 버튼 스타일 */
    .genre-btn {
        width: 100%;
        height: 40px;
        background-color: #FFFFFF;
        color: #0047AB;
        border: 1px solid #0047AB;
        border-radius: 8px;
        font-weight: 700;
        margin-bottom: 8px;
        cursor: pointer;
    }
    .genre-btn:hover {
        background-color: #0047AB;
        color: #FFFFFF;
    }
    </style>
    <div class="top-bar"></div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">실시간 이슈 분석 대시보드</div>', unsafe_allow_html=True)
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
st.markdown(f'<div class="update-time">데이터 기준: {now}</div>', unsafe_allow_html=True)

# --- 데이터 수집 ---
def get_realtime_keywords():
    try:
        url = "https://api.signal.bz/news/realtime"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        return [item['keyword'] for item in res.json()['top10']]
    except:
        return [f"실시간 키워드 {i+1}" for i in range(10)]

keywords = get_realtime_keywords()

# --- 상단: 🔥 실시간 TOP 10 버튼 (2열 배치) ---
st.markdown('<div class="section-header">🔥 실시간 인기 키워드 TOP 10</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
for i, kw in enumerate(keywords):
    with (col1 if i < 5 else col2):
        link = f"https://www.google.com/search?q={quote(kw)}"
        st.markdown(f'<a href="{link}" target="_blank" style="text-decoration:none;"><button class="search-btn">#{i+1} {kw}</button></a>', unsafe_allow_html=True)

# --- 하단: 📂 카테고리별 버튼 ---
genres = {
    "⚖️ 사회": ["민생 지원 대책", "의료 개혁 현황", "대중교통 요금", "기후 위기 대응", "지방 소멸 방지"],
    "💰 경제": ["코스피 전망", "기준 금리 추이", "기술 창업 지원", "엔저 영향 분석", "부동산 세제 개편"],
    "🧬 IT/과학": ["생성형 AI 트렌드", "바이오 의약품 임상", "지식재산권 보호", "반도체 신기술", "우주 항공 산업"],
    "🎬 연예": ["K-콘텐츠 글로벌", "신작 드라마 라인업", "박스오피스 순위", "OTT 신규 요금제", "음원 차트 현황"],
    "⚽ 스포츠": ["해외파 경기 일정", "프로야구 순위 싸움", "챔피언스리그 대진", "올림픽 준비 현황", "e스포츠 대회"]
}

st.markdown('<div class="section-header">📂 카테고리별 인기 검색어</div>', unsafe_allow_html=True)
cols = st.columns(5) # 5개 카테고리를 가로로 배치
for i, (genre, kws) in enumerate(genres.items()):
    with cols[i]:
        st.markdown(f'<p style="text-align:center; font-weight:800; color:#0047AB; margin-bottom:15px;">{genre}</p>', unsafe_allow_html=True)
        for kw in kws:
            link = f"https://www.google.com/search?q={quote(kw)}"
            st.markdown(f'<a href="{link}" target="_blank" style="text-decoration:none;"><button class="genre-btn">{kw}</button></a>', unsafe_allow_html=True)