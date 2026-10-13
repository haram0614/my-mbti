
import streamlit as st
from urllib.error import URLError

st.set_page_config(
    page_title="MBTI 포켓몬 단짝 찾기",
    page_icon="⚡",
    layout="centered",
)

# --------------------------------------------------
# 스타일
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;600;800&display=swap');

.stApp {
    background: linear-gradient(
        180deg, #fff4bd 0%, #fff9e9 38%, #fff9e9 100%
    );
    color: #302b24;
}

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

h1, h2, h3 {
    font-family: 'Jua', sans-serif !important;
    color: #302b24;
}

.block-container {
    max-width: 900px;
    padding-top: 2rem;
}

.hero {
    text-align: center;
    padding: 1.7rem 1rem 1.4rem;
    border: 1px solid #eadfc8;
    border-radius: 26px;
    background: rgba(255,253,247,.88);
    box-shadow: 0 8px 0 #f0e4c9;
    margin-bottom: 1.4rem;
}

.pill {
    display: inline-block;
    padding: .35rem .8rem;
    border-radius: 99px;
    background: #fff0a5;
    font-weight: 800;
    font-size: .82rem;
}

.hero p {
    color: #756d60;
    font-size: 1.05rem;
    margin-bottom: 0;
}

div[data-testid="stButton"] button {
    border-radius: 14px;
    border: 1px solid #eadfc8;
    background: #fffdf7;
    color: #302b24;
    font-weight: 800;
    min-height: 3rem;
    transition: all .15s ease;
}

div[data-testid="stButton"] button:hover {
    border-color: #d2b23b;
    background: #fff0a5;
    color: #302b24;
    transform: translateY(-2px);
}

div[data-testid="stButton"] button[kind="primary"] {
    background: #326b57;
    color: white;
    border: 0;
}

.info-card {
    background: #fff8e8;
    border: 1px solid #eadfc8;
    border-radius: 16px;
    padding: 1rem;
    height: 100%;
}

.muted {
    color: #756d60;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 제목
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <span class="pill">PERSONALITY × POKÉMON</span>
    <h1 style="font-size:2.8rem;margin:.6rem 0 .3rem;">
        나와 찰떡궁합인 포켓몬은?
    </h1>
    <p>나의 MBTI를 선택하고 운명의 단짝 포켓몬을 만나 봐! 💛</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 포켓몬 공식 아트워크
#
# PokeAPI GitHub 공식 아트워크 경로를 사용합니다.
# 이미지 URL 형식:
# https://raw.githubusercontent.com/PokeAPI/sprites/master/
# sprites/pokemon/other/official-artwork/도감번호.png
# --------------------------------------------------

POKEMON_IMAGE_BASE = (
    "https://raw.githubusercontent.com/PokeAPI/sprites/master/"
    "sprites/pokemon/other/official-artwork"
)

def get_pokemon_image_url(pokemon_id):
    """전국도감 번호를 이용해 포켓몬 아트워크 URL을 생성합니다."""
    return f"{POKEMON_IMAGE_BASE}/{pokemon_id}.png"


# --------------------------------------------------
# MBTI 데이터
# --------------------------------------------------

POKEMON = {
    "ISTJ": {
        "ko": "꼬부기", "en": "Squirtle", "id": 7,
        "type": "물", "trait": "차분하고 책임감 있는 실천가",
        "why": "계획을 세우고 맡은 일을 꾸준히 해내는 모습이 꼬부기와 닮았어요. 작은 일도 차근차근 해내는 믿음직한 단짝이에요.",
        "good": "ESFP", "other": "ENFP",
    },
    "ISFJ": {
        "ko": "이브이", "en": "Eevee", "id": 133,
        "type": "노말", "trait": "다정하고 세심한 조력자",
        "why": "주변을 세심하게 살피고 소중한 사람을 챙기는 다정함이 이브이와 잘 어울려요. 함께할수록 서로의 장점을 발견하는 단짝이에요.",
        "good": "ESFP", "other": "ENTP",
    },
    "INFJ": {
        "ko": "가디안", "en": "Gardevoir", "id": 282,
        "type": "에스퍼·페어리", "trait": "깊이 생각하는 이상주의자",
        "why": "다른 사람의 마음을 이해하고 자신만의 가치와 이상을 소중히 여기는 모습이 가디안과 닮았어요. 조용하지만 깊은 유대감을 쌓는 조합이에요.",
        "good": "ENFP", "other": "ESTP",
    },
    "INTJ": {
        "ko": "뮤츠", "en": "Mewtwo", "id": 150,
        "type": "에스퍼", "trait": "전략적인 분석가",
        "why": "큰 그림을 생각하고 복잡한 문제의 원리를 파악하려는 모습이 뮤츠의 지적인 이미지와 어울려요. 목표를 세우면 깊이 파고드는 멋진 단짝이에요.",
        "good": "ENTP", "other": "ESFP",
    },
    "ISTP": {
        "ko": "루카리오", "en": "Lucario", "id": 448,
        "type": "격투·강철", "trait": "침착한 문제 해결사",
        "why": "직접 관찰하고 원리를 익힌 뒤 필요한 순간에 실력을 발휘하는 점이 루카리오와 닮았어요. 말보다 행동으로 신뢰를 쌓는 조합이에요.",
        "good": "ESTJ", "other": "ENFJ",
    },
    "ISFP": {
        "ko": "님피아", "en": "Sylveon", "id": 700,
        "type": "페어리", "trait": "감각적이고 다정한 예술가",
        "why": "자신의 취향과 감정을 소중히 여기며 부드럽게 주변과 어울리는 모습이 님피아와 잘 맞아요. 서로의 개성을 존중하는 단짝이에요.",
        "good": "ESFJ", "other": "ENTJ",
    },
    "INFP": {
        "ko": "쉐이미", "en": "Shaymin", "id": 492,
        "type": "풀", "trait": "마음 따뜻한 몽상가",
        "why": "상상력이 풍부하고 자신이 중요하게 여기는 가치를 지키려는 모습이 쉐이미의 사랑스러운 분위기와 닮았어요. 함께 작은 행복을 발견하는 단짝이에요.",
        "good": "ENFJ", "other": "ESTJ",
    },
    "INTP": {
        "ko": "메타몽", "en": "Ditto", "id": 132,
        "type": "노말", "trait": "호기심 많은 탐구자",
        "why": "정해진 틀에 얽매이지 않고 여러 가능성을 실험하며 원리를 탐구하는 모습이 메타몽과 어울려요. 엉뚱한 아이디어를 마음껏 나누는 조합이에요.",
        "good": "ENTJ", "other": "ESFJ",
    },
    "ESTP": {
        "ko": "리자몽", "en": "Charizard", "id": 6,
        "type": "불꽃·비행", "trait": "대담한 행동가",
        "why": "생생한 경험을 즐기고 기회가 오면 과감하게 움직이는 에너지가 리자몽과 닮았어요. 새로운 모험에 함께 뛰어드는 단짝이에요.",
        "good": "ISFJ", "other": "INFJ",
    },
    "ESFP": {
        "ko": "피카츄", "en": "Pikachu", "id": 25,
        "type": "전기", "trait": "활기찬 분위기 메이커",
        "why": "사람들과 함께하는 순간을 즐기고 주변에 밝은 에너지를 전하는 모습이 피카츄와 잘 어울려요. 함께라면 평범한 하루도 모험이 돼요.",
        "good": "ISTJ", "other": "INTJ",
    },
    "ENFP": {
        "ko": "푸린", "en": "Jigglypuff", "id": 39,
        "type": "노말·페어리", "trait": "상상력 넘치는 아이디어 뱅크",
        "why": "새로운 가능성을 발견하고 감정을 표현하며 사람들을 즐겁게 하는 모습이 푸린과 닮았어요. 재미있는 아이디어와 웃음이 끊이지 않는 단짝이에요.",
        "good": "INFJ", "other": "ISTJ",
    },
    "ENTP": {
        "ko": "팬텀", "en": "Gengar", "id": 94,
        "type": "고스트·독", "trait": "재치 있는 발명가",
        "why": "남들이 당연하게 여기는 것도 다르게 바라보고 기발한 아이디어를 내는 모습이 팬텀과 어울려요. 장난과 토론을 즐기는 유쾌한 조합이에요.",
        "good": "INTJ", "other": "ISFJ",
    },
    "ESTJ": {
        "ko": "윈디", "en": "Arcanine", "id": 59,
        "type": "불꽃", "trait": "든든한 리더",
        "why": "목표를 분명히 하고 팀을 이끌며 책임감 있게 행동하는 모습이 늠름한 윈디와 닮았어요. 서로 믿고 힘차게 나아가는 단짝이에요.",
        "good": "ISTP", "other": "INFP",
    },
    "ESFJ": {
        "ko": "해피너스", "en": "Blissey", "id": 242,
        "type": "노말", "trait": "따뜻한 돌봄이",
        "why": "사람들을 챙기고 모두가 편안하게 지낼 수 있도록 돕는 모습이 해피너스와 잘 맞아요. 서로를 응원하고 마음을 나누는 단짝이에요.",
        "good": "ISFP", "other": "INTP",
    },
    "ENFJ": {
        "ko": "루카리오", "en": "Lucario", "id": 448,
        "type": "격투·강철", "trait": "마음을 움직이는 리더",
        "why": "사람들의 가능성을 발견하고 함께 성장하도록 이끄는 모습이 루카리오의 의리 있는 이미지와 어울려요. 서로를 믿고 목표를 향해 나아가는 조합이에요.",
        "good": "INFP", "other": "ISTP",
    },
    "ENTJ": {
        "ko": "보만다", "en": "Salamence", "id": 373,
        "type": "드래곤·비행", "trait": "목표 지향적인 전략가",
        "why": "높은 목표를 세우고 큰 그림을 향해 추진력을 발휘하는 모습이 하늘을 향해 날아오르는 보만다와 닮았어요. 큰 꿈을 함께 응원하는 단짝이에요.",
        "good": "INTP", "other": "ISFP",
    },
}

ORDER = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ",
]

# --------------------------------------------------
# 상태 초기화
# --------------------------------------------------

if "selected_mbti" not in st.session_state:
    st.session_state.selected_mbti = "ENFP"

if "show_result" not in st.session_state:
    st.session_state.show_result = False

# --------------------------------------------------
# MBTI 선택
# --------------------------------------------------

st.subheader("🧩 1. 나의 MBTI를 골라 줘")
st.caption("16가지 유형 중 하나를 선택하세요. 선택하면 표시가 바뀝니다.")

cols = st.columns(4)

for i, mbti in enumerate(ORDER):
    with cols[i % 4]:
        is_selected = st.session_state.selected_mbti == mbti

        if st.button(
            ("⭐ " if is_selected else "") + mbti,
            key=f"mbti_{mbti}",
            use_container_width=True,
            type="primary" if is_selected else "secondary",
        ):
            st.session_state.selected_mbti = mbti
            st.session_state.show_result = False
            st.rerun()

left, right = st.columns([3, 2])

with left:
    if st.button(
        "✨ 나의 단짝 포켓몬 찾기!",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.show_result = True

with right:
    if st.button("🔄 다시 고르기", use_container_width=True):
        st.session_state.selected_mbti = "ENFP"
        st.session_state.show_result = False
        st.rerun()

# --------------------------------------------------
# 결과 화면
# --------------------------------------------------

if st.session_state.show_result:
    mbti = st.session_state.selected_mbti
    p = POKEMON[mbti]

    st.balloons()
    st.markdown("---")
    st.markdown(f"## 🎉 축하해! {mbti}의 단짝 포켓몬을 찾았어!")
    st.caption("두근두근… 운명의 파트너 공개!")

    image_url = get_pokemon_image_url(p["id"])

    c1, c2 = st.columns([1, 1.4], gap="large")

    with c1:
        try:
            st.image(
                image_url,
                caption=f"{p['ko']} ({p['en']})",
                use_container_width=True,
            )
        except (OSError, URLError, RuntimeError):
            st.warning("이미지를 불러오지 못했어요. 인터넷 연결을 확인해 주세요.")
            st.link_button(
                "포켓몬 공식 아트워크 열기",
                image_url,
                use_container_width=True,
            )

    with c2:
        st.markdown(f"### 💛 {p['ko']} ({p['en']})")
        st.markdown(f"**타입:** {p['type']}")
        st.markdown(f"**특징:** {p['trait']}")
        st.markdown("**너와 어울리는 이유**")
        st.write(p["why"])

    # 궁합
    st.markdown("### 🤝 단짝 궁합")

    a, b = st.columns(2)

    with a:
        st.markdown(
            f"""
            <div class="info-card">
                <div>🌟 <b>잘 맞을 수 있는 유형</b></div>
                <h3>{p['good']}</h3>
                서로의 장점을 보완하고 함께 성장할 수 있는 조합으로 골랐어요.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with b:
        st.markdown(
            f"""
            <div class="info-card">
                <div>🌈 <b>새로운 관점을 주는 유형</b></div>
                <h3>{p['other']}</h3>
                다른 생각을 나누면서 새로운 아이디어를 얻을 수 있어요.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.info(
        "참고: 포켓몬 매칭과 MBTI 궁합은 재미를 위한 창작 콘텐츠이며, "
        "공식 진단이나 과학적 판정이 아닙니다."
    )

    st.markdown("""
    <div style="
        text-align:center;
        background:#fff0a5;
        border-radius:18px;
        padding:1rem;
        margin-top:1rem;
    ">
        <span style="font-size:1.5rem;">🌟 🎊 💛 🎊 🌟</span><br>
        <b>새로운 단짝과 즐거운 모험을 시작해 봐!</b>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="info-card" style="text-align:center;margin-top:1rem;">
        <div style="font-size:2.3rem;">🎁</div>
        <b>아직 단짝 포켓몬이 비밀에 싸여 있어!</b><br>
        아래 버튼을 누르면 축하 효과와 함께 결과가 공개돼.
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# 하단 안내
# --------------------------------------------------

st.markdown("""
<p style="
    text-align:center;
    color:#756d60;
    font-size:.8rem;
    margin-top:2rem;
">
    포켓몬 이미지 출처:
    <a href="https://github.com/PokeAPI/sprites/tree/master/sprites/pokemon/other/official-artwork"
       target="_blank">PokéAPI 공식 아트워크 저장소</a><br>
    이미지를 표시하려면 인터넷 연결이 필요합니다.<br>
    MBTI는 재미로 즐기는 성격 유형 콘텐츠입니다. 💛
</p>
""", unsafe_allow_html=True)
