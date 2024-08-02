import cv2
import numpy as np

def main():

    src = cv2.imread('C:/Users/CHO_YUBIN/PycharmProjects/Internship/alignment.png')
    dst = src.copy()
    gray_img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    blurred_img = cv2.GaussianBlur(gray_img, (5, 5), 0)  # 노이즈 제거

    # 1. 객체(사각형) 탐지 및 라벨링
    _, threshed_img1 = cv2.threshold(blurred_img, 254, 255, cv2.THRESH_BINARY_INV)    # 정확도 높이기 위해 binary 이미지 사용
    # 254: threshold값
    # 255: threshold보다 클 때 나타낼 값

    # OpenCV에서 contours(등고선)를 찾는 건 검은색 배경에서 흰색 객체를 찾는 것
    # → 배경은 검은색, 객체는 흰색이어야 함 (https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html)

    contours, _ = cv2.findContours(threshed_img1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # (입력 영상, 컨투어 제공 방식 (cv2.RETR_EXTERNAL: 외곽 윤곽선만 검출, 계층 구조 구성 X), 근사화 방식 (cv2.CHAIN_APPROX_NONE: 근사 없이 모든 모든 윤곽점 반환)
    rectangle_detection = src.copy()  # 사각형 검출 위한 이미지. drawContours()는 입력 이미지를 직접 수정하므로 입력 이미지를 보존하려면 결과 이미지 출력을 위해 copy해서 사용해야 함
    cv2.drawContours(rectangle_detection, contours, -1, (0, 0, 255), 10)
    # (image, findContours로 구한 contours(contour의 좌표 정보), contour의 인덱스 (-1: 모든 contour 출력), 색상, 두께 (-1: 내부 채움))

    # print("1번째 객체 검출: " + str(len(contours)))


    for index, contour in enumerate(contours):

        # 2. 사각형 객체 크기별로 클래스 분류하기
        area = cv2.contourArea(contour)
        # print(area)

        if area <= 53000:
            rectangle_class = 'A'
        elif area <= 150000:
            rectangle_class = 'B'
        elif area <= 250000:
            rectangle_class = 'C'
        # else area <= 640000:
        else:
            rectangle_class = 'D'

        # 객체, 클래스별 라벨링
        x_2d = contour.T[0]
        x_1d = [a for i in x_2d for a in i]  # 2차원 배열 1차원 배열로
        min_x_index = x_1d.index(np.min(x_1d))

        y_2d = contour.T[1]
        y_1d = [a for i in y_2d for a in i]
        min_y_index = y_1d.index(np.min(y_1d))
        max_y_index = y_1d.index(np.max(y_1d))

        # +) 결과를 사각형 객체 좌측 상단에 표시

        # 1. 객체가 오른쪽으로 기울어져 있는 경우
        # 객체에서 y가 최소일 때 x < y가 최대 → 결과가 출력되어야 하는 x는 y가 최소일 때 x좌표, y는 y가 최소일 때 y좌표
        # 2. 객체가 왼쪽으로 기울어져 있는 경우
        # 객체에서 y가 최소일 때 y > y가 최대 → 결과가 출력되어야 하는 x는 x가 최소일 때 x좌표, y는 x가 최소일 때 y좌표
        # 3. 객체가 기울어져 있지 않은 경우
        # 객체에서 y가 최소일 때 y = y가 최대 → 결과가 출력되어야 하는 x는 x가 최소일 때 x좌표, y는 y가 최소일 때 y좌표
        # cv2.findContours에서 반환되는 contour들의 좌표 특성상 3번은 따로 명시해주지 않고 2번을 else로 묶어줘도 상관은 X

        if x_1d[min_y_index] < x_1d[max_y_index]:
            x_text_coordinate = x_1d[min_y_index]
            y_text_coordinate = np.min(y_1d)
        elif x_1d[min_y_index] > x_1d[max_y_index]:
            x_text_coordinate = np.min(x_1d)
            y_text_coordinate = y_1d[min_x_index]
        else:
            x_text_coordinate = np.min(x_1d)
            y_text_coordinate = np.min(y_1d)

        cv2.putText(dst, "No. " + str(index + 1) + " Class " + str(rectangle_class), org=tuple([x_text_coordinate - 50, y_text_coordinate - 25]), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=4, color=(0, 0, 0), thickness=3)
        # org: 쓸 문자열의 왼쪽 아래 (-50, -20은 왼쪽 위로 여백 줘서 띄우기 위함)

    # 3. 패턴 매칭으로 십자가 이미지 찾기
    cross = cv2.imread('C:/Users/CHO_YUBIN/PycharmProjects/Internship/cross.png')
    gray_cross = cv2.cvtColor(cross, cv2.COLOR_BGR2GRAY)
    _, threshed_cross = cv2.threshold(gray_cross, 254, 255, cv2.THRESH_BINARY_INV)
    # 정확도 높이기 위해 binary 이미지 사용 (검은색 십자가 영상이므로 반전)

    _, threshed_img2 = cv2.threshold(blurred_img, 120, 255, cv2.THRESH_BINARY_INV)  # 십자가 검출용 thresholding

    contours, _ = cv2.findContours(threshed_img2, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # (cv2.RETR_LIST: 모든 윤곽선 검출, 계층 구조 구성 X)

    cross_detection = src.copy()  # 십자가 검출 위한 이미지
    cv2.drawContours(cross_detection, contours, -1, (0, 0, 255), 10)

    cross_contours, _ = cv2.findContours(threshed_cross, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # print("2번째 객체 검출: " + str(len(contours)))

    # 검출된 십자가 객체마다 빨간색 원으로 표시
    for contour in contours:

        difference = cv2.matchShapes(cross_contours[0], contour, cv2.CONTOURS_MATCH_I3, 0)
        # matchShapes: 두 contour가 비슷할수록 0에 가까운 값 반환
        # matchShapes 함수는 I3(3번째 방법)가 정규화를 이용하므로 효과가 가장 좋다고 알려져 있음

        if difference < 0.1:
            (x, y), radius = cv2.minEnclosingCircle(contour)    # 원의 중심 좌표, 반지름 반환
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(dst, center, radius, color=(0, 0, 255), thickness=3)

    # 화면에 출력하기 위해 사이즈 조절
    src = cv2.resize(src, dsize=(0, 0), fx=0.3, fy=0.3)
    dst = cv2.resize(dst, dsize=(0, 0), fx=0.3, fy=0.3)
    rectangle_detection = cv2.resize(rectangle_detection, dsize=(0, 0), fx=0.3, fy=0.3)
    cross_detection = cv2.resize(cross_detection, dsize=(0, 0), fx=0.3, fy=0.3)
    threshed_img1 = cv2.resize(threshed_img1, dsize=(0, 0), fx=0.3, fy=0.3)
    threshed_img2 = cv2.resize(threshed_img2, dsize=(0, 0), fx=0.3, fy=0.3)

    cv2.imshow('src', src)  # 입력 이미지
    # cv2.imshow('threshed_img1', threshed_img1)  # 사각형 검출 위한 thresholding
    # cv2.imshow('threshed_img2', threshed_img2)  # 십자가 검출 위한 thresholding
    # cv2.imshow('rectangle_detection', rectangle_detection)    # 사각형 검출 결과
    # cv2.imshow('cross_detection', cross_detection)  # 십자가 검출 결과
    cv2.imshow('dst', dst)  # 결과 이미지

    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
