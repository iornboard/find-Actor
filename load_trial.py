import dlib, cv2 # (얼굴 추척, 인식),(이미지 처리 작업)
import numpy as np # 행렬 연산을 위해서(이미지 처리)
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import matplotlib.patheffects as patches_effects
import database as db

font_path = 'ect\Cafe24Ohsquare.ttf'   # 폰트 위치
fontprop = fm.FontProperties (fname=font_path, size=18)


detector = dlib.get_frontal_face_detector()  # 모듈 위치
sp = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('models/dlib_face_recognition_resnet_model_v1.dat')


def find_face(img):  # 얼굴을 찾는 함수
  dets = detector(img, 1)  # dets에 얼굴 찾은 결과물이 들어감

  if len(dets) == 0:
    return np.empty(0), np.empty(0), np.empty(0)  # 못 찾을 경우 빈 배열을 반환

  rects, shapes = [], []  # 저장할 배열  (!)

  shapes_np = np.zeros((len(dets), 68, 2), dtype=np.int)  # 얼굴의 점(랜드마크)가 보통 68개  (!)

  for k, d in enumerate(dets):
    rect = ((d.left(), d.top()), (d.right(), d.bottom()))  # 랜드마크를 순회하면서 가장자리를 찾는다.
    rects.append(rect)

    shape = sp(img, d)  # (이미지, 사각형) >> 68개의 랜드마크를 추출

    for i in range(0, 68):
      shapes_np[k][i] = (shape.part(i).x, shape.part(i).y)

    shapes.append(shape)

  return rects, shapes, shapes_np


def encode_face(img, shapes):  # 얼굴 인코딩 함수  (이미지를 백터 데이터로 변환 )
  face_descriptors = []
  for shape in shapes:  #
    face_descriptor = facerec.compute_face_descriptor(img, shape)  # 랜드마크와 이미지를 넣는다.
    face_descriptors.append(np.array(face_descriptor))

  return np.array(face_descriptors)  # 이미지당 랜드마크 비교 + 인코딩 값 반환


def save_desce() :
  for name, img_path in db.img_paths.items():
    img_bgr = cv2.imread(img_path)  # imread => 이미지를 로드하는 함수(출력 : bgr형식으로 나온다.)
    img_rbg = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)  # BGR 이미지을 RBG형식으로 변환한다.

    _, img_shapes, _ = find_face(img_rbg)
    db.descs[name] = encode_face(img_rbg, img_shapes)[0]  # (?)

  np.save('img/descs.npy', db.descs)



def main_recog(img) :
  Main_img_bgr = cv2.imread(img)  # 검사할 이미지 위치
  Main_img_rbg = cv2.cvtColor(Main_img_bgr, cv2.COLOR_BGR2RGB)

  rects, shapes, _ = find_face(Main_img_rbg)
  descriptors = encode_face(Main_img_bgr, shapes)


  fig, ax =  plt.subplots(1, figsize =(20,20))
  ax.imshow(Main_img_rbg)

  for i, desc in enumerate(descriptors) :


    for name, saved_desc in db.descs.items() :
      dist = np.linalg.norm([desc] - saved_desc,axis=1) # 그냥 쓴 함수  // 자세한건 잘 모르겠어요
      found = False

      if dist < 0.49555:    # << 정확도
        found = True

        text = ax.text(rects[i][0][0], rects[i][0][1],name,
                       color = "blue", fontsize =40, fontweight= 'bold', fontproperties=fontprop)
        text.set_path_effects([patches_effects.Stroke(linewidth=1, foreground='white')])

        rect = patches.Rectangle(rects[i][0],
                                 rects[i][1][1] - rects[i][0][1],
                                 rects[i][1][0] - rects[i][0][0],
                                 linewidth = 2 ,edgecolor = "white" , facecolor='none'  )
        db.cator_list.append(name)
        ax.add_patch(rect)

        break

      if not found :
        text = ax.text(rects[i][0][0], rects[i][0][1], 'unknown',
                       color = 'r', fontsize = 20, fontweight = 'bold', fontproperties=fontprop)
        rect = patches.Rectangle(rects[i][0],
                                 rects[i][1][1] - rects[i][0][1],
                                 rects[i][1][0] - rects[i][0][0],
                                 linewidth=2, edgecolor='r', facecolor='none')

        ax.add_patch(rect)


  plt.show()
