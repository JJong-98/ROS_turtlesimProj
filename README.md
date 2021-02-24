Winter Proj _ ROS Turtlesim
====================
_(21/02/24)
------------------------------------------------
> 터틀심 실행
> 화면을 9분할 하여 해당 부분의 색상을 추출
> 색상이 추출한 위치로 터틀심을 이동

### 실행 방법

`roslaunch <pkg> project.launch`

#### src : project1.py
[project1.py](https://github.com/yannJu/ROS_turtlesimProj/blob/master/launch/project.launch)

* image_callback : 웹캠을 통해 들어온 이미지를 변환
* pose_callback : turtle의 좌표
* control_msg_publish : turtle을 이동시키기 위한 pub 함수
* getAngle, getDistance : 현재좌표 - 색상이 추출된 좌표(가야할 좌표) 사이의 거리와 방향을 측정
	- 해당 값을 얻음으로서 원하는 좌표로 이동하는데 사용
* setDir : turtle의 방향을 set -> turtle의 이동거리 set

#### launch : project.launch
[project.launch](https://github.com/yannJu/ROS_turtlesimProj/blob/master/src/project1.py)

```
usb_cam 의 작동이 느림 : usb_cam이 멈춘동안 turtle은 방향을 잡지못함
turtle의 방향 문제 : 비율로 linear.x와 angular.z를 설정 => 잘못된 위치로 이동
nan : 물건이 사라질경우의 예외처리가 올바르지 않음 => nan으로 인해 turtle의 좌표도 nan이 되어버릴 경우 제대로 프로그램이 작동되지 않음
```

