# turtlebot3_sonar
turtlebot3に超音波センサを取り付けrosトピックとして取り扱うためのドキュメント \
最終更新日：2022/11/14

## 確認済み環境確認
- Ubuntu20.04
- ROS noetic
- 超音波センサ "HC-SR04"
- Turtlebot3-waffle-pi
- Turtlebot3のパッケージをインストールして動作済みであることを確認してください \
https://github.com/ROBOTIS-GIT/turtlebot3
- turtlebot3_applicationsについてもインストールをしてください \
https://github.com/ROBOTIS-GIT/turtlebot3_applications \
https://github.com/ROBOTIS-GIT/turtlebot3_applications_msgs


## 超音波センサの取り付け
配線は以下の図を参照。

## turtlebot内のソースについて
turtlebot3_bringupパッケージにsonar_pub.pyを入れる。 \
turtlebot_bringup.launchを入れ替える

## remote pc内のソースについて
### move_base使用時の緊急停止用として使う
sonar_stop.pyを参照してください。

### ARマーカーによる原点復帰用として使う
automatic_parking_vision2.pyを参照してください。
  