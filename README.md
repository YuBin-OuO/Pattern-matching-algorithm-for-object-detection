## 🗓️ 과제 기간
2023/7/17 ~ 2023/7/23

## 🛠️ 사용 언어 및 기술
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/OpenCV-27338e?style=flat-square&logo=OpenCV&logoColor=white"/> <img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white"/>

## 💫 설명
### 요구사항
1. blob 이용하여 대상 넘버링(no)하기
2. 특정 크기로 네이밍(class)하기
3. 패턴매칭하여 사각형 안의 특정 이미지(십자가) 찾기

이미지는 사각형 총 10개 이상, 크기 4종류, 패턴매칭 십자가 2개를 만들 것
결과는 사각형 좌측 상단에 no, class를 표시해 보여주고 저장할 것
패턴매칭으로 찾은 것은 빨간색 원으로 표시할 것

### 해결방법
- 사각형 객체를 탐지하기 위해서 OpenCV 내장함수인 findContours()를 이용  
(Blob Detection을 위한 SimpleBlobDetector()를 이용해도 결과는 같게 나옴)
- 십자가의 contour를 추출한 뒤, 입력 이미지에서 추출한 contour들과의 차이를 matchShapes 함수를 이용해 비교하여 특정값보다 차이가 적으면 십자가로 판단하여 빨간색 원으로 표시

## ✊ 피드백 및 개선 방향
이미지에서 객체를 검출하기 위해 전처리하는 과정과, 객체를 크기별로 네이밍하는 과정에서는 하드코딩식으로 파라미터를 입력해줬는데, 이 부분은 보완이 필요할 듯
