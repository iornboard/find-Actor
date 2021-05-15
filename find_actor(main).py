import load_trial as recog
import 와챠검색 as sear
import database as db

recog.save_desce()
recog.main_recog('img/Itaewon.jpg') # << ( )여기에 이미지를 입력

# db.cator_list <!< 이미지에 있는 사람들의 이름들 >!> 리스트로

for index, name in enumerate(db.cator_list) : print("[ {0} : {1} ]".format(index+1,name), end = '' )
num = int(input("\n 누구를 검색하시겠습니까? : "))

sear.main_search(db.cator_list[num-1])