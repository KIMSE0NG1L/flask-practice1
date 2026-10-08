# HW3 — Todo 앱에 수정 기능 더하기

오늘 DB(SQLite)로 옮긴 todo_app 을 복사해 설명(note) 칸과 수정(edit) 화면을 추가했습니다.

## 실행 방법
```
cd HW3
flask run
```

## 고친 곳
- `app.py`
  - `Todo` 모델에 `note` 칸 추가
  - `/` POST 처리에서 `note` 도 같이 저장
  - `/edit/<int:id>` 라우트 추가 (GET: 수정 화면, POST: 저장 후 목록으로)
- `templates/index.html` : 입력 폼에 설명 칸 추가, 목록에 설명과 [수정] 링크 표시
- `templates/edit.html` : 새로 만듦. 기존 값이 채워진 수정 폼
- `static/style.css` : `.note` 클래스 추가

## 명세 확인
- ① 추가 — 할 일 + 설명을 같이 저장
- ② 조회 — DB에서 읽어 목록 표시
- ③ 완료 토글
- ④ 수정 — `/edit/<int:id>`
- ⑤ 삭제

## 실행 화면

### 목록 화면 (설명 칸, [수정] 링크 포함)
![목록](screenshots/list.png)

### 수정 화면
![수정](screenshots/edit.png)

### 서버를 껐다 켠 뒤에도 그대로인 목록
![재시작 후](screenshots/restarted.png)
