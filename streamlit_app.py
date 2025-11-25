import os
import streamlit as st
import google.generativeai as genai

# 1. 환경변수에서 GOOGLE_API_KEY 가져오기 (Streamlit Cloud에서도 동일하게 사용)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY가 설정되어 있지 않습니다. 로컬에서는 터미널에서 환경변수를 설정하거나 .env를 사용하세요.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

    # 2. Gemini 모델 설정 (텍스트용)
    model = genai.GenerativeModel("gemini-2.5-flash")

    # 3. Streamlit UI 설정
    st.set_page_config(page_title="패션 MD 트렌드 리서처", page_icon="👗")

    st.title("👗 패션 MD 자동 트렌드 리서처")
    st.write("패션 MD 관점에서 트렌드 요약과 상품기획 인사이트를 생성하는 간단한 데모입니다.")

    keyword = st.text_input("분석할 키워드를 입력하세요", placeholder="예: 2025 여성 봄 패션 트렌드")

    if st.button("트렌드 분석 시작"):
        if not keyword.strip():
            st.warning("키워드를 입력해주세요.")
        else:
            with st.spinner("Gemini가 트렌드를 분석하는 중입니다... ⏳"):
                prompt = f"""
                당신은 패션 MD입니다.
                아래 키워드에 대해 패션 트렌드 분석 리포트를 작성하세요.

                키워드: {keyword}

                리포트 구성:
                1) 핵심 패션 트렌드 5가지
                2) 연령대별 특징 (10대, 20대, 30대 이상)
                3) 소비자 니즈 정리
                4) 상품기획 아이디어 (소재 / 컬러 / 핏 / 가격대 관점에서)
                5) 실제 MD 인사이트 3개 (재고, 리스크, 기획 방향 포함)

                출력은 마크다운 형식으로 깔끔하게 정리하세요.
                """

                response = model.generate_content(prompt)

            st.success("분석이 완료되었습니다! ✨")
            st.markdown(response.text)
