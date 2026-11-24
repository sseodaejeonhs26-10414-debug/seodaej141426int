"""문화 지킴이: Python 3으로 실행하는 간단한 문화 학습 게임."""

import json
from datetime import date, timedelta
from pathlib import Path


# 제주특별자치도와 유네스코 자료를 바탕으로 정리한 학습 콘텐츠입니다.
# 등재 당시의 위기 요인과 현재의 보호 노력을 구분해 설명합니다.
자료 = {
    "대한민국": {
        "언어": ("제주어", "제주어는 제주 지역의 삶과 문화를 담은 언어예요.\n"
               "위기: 2010년 유네스코가 소멸 위기 언어로 분류했어요. 사용자 감소가 문제예요.\n"
               "보호 방법: 제주어 교육 자료로 배우고 일상에서 사용해 보세요.",
               "제주어 보존에 도움이 되는 행동은?", ["배우고 사용하기", "사용하지 않고 잊기"], 1),
    },
    "아제르바이잔": {
        "전통놀이": ("초브간(Chovqan)", "카라바흐 말을 타고 나무채로 공을 상대 골대에 넣는 팀 놀이예요.\n"
                 "위기: 선수·지도자·말 부족 등으로 2013년 유네스코 긴급보호목록에 올랐어요.\n"
                 "보호 노력: 2026년 보고서에는 선수 증가가 나타나지만 지속적인 전승 지원이 필요해요.\n"
                 "보호 방법: 경기와 문화적 의미를 배우고 전승 교육에 관심을 가져 보세요.",
                 "초브간에서 선수가 타는 동물은?", ["낙타", "말"], 2),
    },
    "과테말라": {
        "축제·의례": ("난 파치 의례(Nan Pa’ch)", "산페드로사카테페케스에서 옥수수 수확에 감사하는 의례예요.\n"
                  "위기: 전승자 고령화와 전승 감소 등으로 2013년 유네스코 긴급보호목록에 올랐어요.\n"
                  "보호 방법: 공동체가 전하는 의례의 의미를 배우고 전승 활동을 존중해 주세요.",
                  "난 파치 의례에서 수확에 감사하는 작물은?", ["옥수수", "벼"], 1),
    },
}
대륙 = {"아시아": ["대한민국", "아제르바이잔"], "북아메리카": ["과테말라"]}
출처 = {
    "대한민국": "제주특별자치도: https://www.jeju.go.kr/jedu/archive/jeju.htm?act=view&seq=21",
    "아제르바이잔": "유네스코: https://ich.unesco.org/en/Decisions/8.COM/7.a.1\n"
                 "2026년 보호 보고서: https://ich.unesco.org/doc/src/76468-EN.pdf",
    "과테말라": "유네스코: https://ich.unesco.org/en/USL/nan-pa-ch-ceremony-00863?USL=00863",
}
저장파일 = Path(__file__).with_name("record.json")


def 선택(질문, 항목):
    print("\n" + 질문)
    for 번호, 이름 in enumerate(항목, 1):
        print(f"{번호}. {이름}")
    while True:
        입력 = input("번호 입력: ").strip()
        if 입력.isdecimal() and 1 <= int(입력) <= len(항목):
            return 항목[int(입력) - 1]
        print("목록에 있는 번호를 입력해 주세요.")


def 기록읽기():
    기본값 = {"포인트": 0, "완료": [], "마지막학습": "", "연속학습": 0}
    try:
        기록 = json.loads(저장파일.read_text(encoding="utf-8"))
        if (not isinstance(기록, dict)
                or type(기록.get("포인트")) is not int
                or 기록["포인트"] < 0
                or not isinstance(기록.get("완료"), list)
                or not all(isinstance(항목, str) for 항목 in 기록["완료"])
                or type(기록.get("연속학습")) is not int
                or 기록["연속학습"] < 0):
            raise ValueError
        date.fromisoformat(기록["마지막학습"])
        return 기록
    except FileNotFoundError:
        return 기본값
    except (OSError, ValueError, TypeError, KeyError):
        print("기록을 읽을 수 없어 새 기록으로 시작합니다.")
        return 기본값


def 실행():
    기록 = 기록읽기()
    print("🌏 문화 지킴이 — 배우고, 풀고, 문화를 지켜요!")
    print("소멸 위기 언어와 긴급보호가 필요한 전통문화를 배워요.")
    print("대한민국: 제주어 / 아제르바이잔: 초브간 / 과테말라: 난 파치 의례")
    while True:
        메뉴 = 선택("메뉴", ["문화 배우기", "내 기록·공유", "문화유산 보호 카드", "종료"])
        if 메뉴 == "종료":
            break
        if 메뉴 == "내 기록·공유":
            배지 = "문화 지킴이 🏅" if len(기록["완료"]) >= 3 else "문화 탐험가 🌱"
            연속 = 기록["연속학습"] if 기록["마지막학습"] in (
                date.today().isoformat(), (date.today() - timedelta(days=1)).isoformat()) else 0
            print(f"\n[공유용 문구] {배지} | {기록['포인트']}점 | 레벨 {기록['포인트'] // 30 + 1}")
            print(f"완료한 학습 {len(기록['완료'])}개 · 연속 학습 {연속}일")
            print("이 문구를 복사해 공유해 보세요!")
        elif 메뉴 == "문화유산 보호 카드":
            print("\n🌊 침수 · 부식 · 산불은 문화유산을 위협할 수 있어요.")
            print("보호 활동: 관람 규칙 지키기, 쓰레기 줄이기, 보호의 필요성 알리기")
        else:
            지역 = 선택("대륙 선택", list(대륙))
            나라 = 선택("나라 선택", 대륙[지역])
            분야 = 선택("학습 분야 선택", ["언어", "전통놀이", "축제·의례"])
            if 분야 not in 자료[나라]:
                추천 = [국가 for 국가, 내용 in 자료.items() if 분야 in 내용]
                print("아직 자료가 없습니다. 추천 국가: " + ", ".join(추천))
                continue
            제목, 설명, 질문, 보기, 정답 = 자료[나라][분야]
            print(f"\n📖 {제목}\n{설명}")
            print(f"출처: {출처[나라]}")
            답 = 선택(질문, 보기)
            if 답 != 보기[정답 - 1]:
                print(f"아쉬워요! 정답: {보기[정답 - 1]}\n다시 도전해 보세요.")
                continue
            print("정답입니다!")
            학습번호 = f"{나라}/{제목}"
            오늘 = date.today().isoformat()
            어제 = (date.today() - timedelta(days=1)).isoformat()
            if 학습번호 not in 기록["완료"]:
                기록["완료"].append(학습번호)
                기록["포인트"] += 10
                print("새 학습 완료! +10점")
            if 기록["마지막학습"] != 오늘:
                기록["연속학습"] = 기록["연속학습"] + 1 if 기록["마지막학습"] == 어제 else 1
                기록["마지막학습"] = 오늘
                기록["포인트"] += 5
                print("오늘의 미션: 퀴즈 하나 맞히기 완료! +5점")
            try:
                저장파일.write_text(json.dumps(기록, ensure_ascii=False, indent=2), encoding="utf-8")
            except OSError:
                print("기록을 저장하지 못했습니다. 폴더의 쓰기 권한을 확인해 주세요.")


if __name__ == "__main__":
    try:
        실행()
    except (EOFError, KeyboardInterrupt):
        print("\n프로그램을 종료합니다.")
