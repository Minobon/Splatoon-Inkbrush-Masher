# Splatoon-Inkbrush-Masher

プロコンでのZR連打を補助してくれるプログラム。パブロとかが使いやすくなる。  
ZR単押しと長押しを区別して連打するかどうか判断することで、ZR以外のボタンを使うことなく連打と筆移動両方が可能。
その辺の連射コンでは出来ないと思う。知らんけど。  

Swicth - Raspberry Pi - Procon  
というようにラズパイを中継して接続し、途中でデータを書き換えることで連射機能を実装している。

## 導入方法
#### 用意するもの
- Raspberry Pi 4B (**おすすめ**) または Raspberry Pi Zero/Zero2
  - 僕はZeroで色々苦労しました。出来なくはないんだけどね。
- プロコン
- USBケーブル(A to C) 2本
  - ドックとラズパイ、ラズパイとプロコンが繋げられればOK  

#### 最初だけする作業
OS（Raspbian）のUSB gadgetという機能を使いたいので、それを有効化する作業。  
コマンドラインで以下のコマンド3つをそれぞれ実行する。  
~~~
echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
echo "libcomposite" | sudo tee -a /etc/modules
~~~
出来たらラズパイを再起動。  
その後 [add_procon_gadget.sh](https://gist.github.com/mzyy94/60ae253a45e2759451789a117c59acf9#file-add_procon_gadget-sh) をここからダウンロードする

#### 毎回やること
ダウンロードしておいた `add_procon_gadget.sh` を実行する。
~~~
sudo sh add_procon_gadget.sh
~~~
このときSwitchとラズパイのUSB Type-CポートをUSBケーブルで繋いでおく。  
  
特にエラーなく実行出来たら、以下のプログラム `Mash-n-times.py` `Toggle-masher.py` のうち好きな方を実行する。  
~~~
sudo python3 Mash-n-times.py
~~~
このときプロコンとラズパイをUSBケーブルで繋いでおく。  


&nbsp;
## Mash-n-times.py
ZRを単押しするとconfigで設定した回数連打してくれる。  
シンプルで慣れもあまり必要なく使いやすいが、連打が終わるまでイカになれない為、体感上筆を振った後一瞬硬直状態になる（スクリュースロッシャーぽい使用感）。  
長押しとの区別は、ZRを離した時点でZRが何ミリ秒押されていたか。閾値はconfigで設定する。  

### Config (23行目~30行目)
~~~
#Judgment threshold (in ms).
config_ms = 300

#Number of shots (in integer).
config_count = 3

#Toggle key
config_key = 'p'
~~~
|変数名|説明|初期値|
----|----|---- 
|config_ms|ZRを押した時間がどれだけ以下なら単押しと判定するか (ms)|300|
|config_count|ZRを単押しした場合何回連打入力するか (整数)|3|
|config_key|Raspberry Piに接続したキーボードのどのキーを押せば<br>機能をオンオフ出来るか (任意のキーの1文字)|p|

&nbsp;
## Toggle-masher.py（鋭意製作中）
ZRを単押しするごとに連打機能をオン/オフしてくれる。  
慣れが必要だが筆を振った後の硬直を最小限に出来るメリットがある。  
長押しとの区別は`Mash-n-times.py`と同じ方法。configの設定も同様。

&nbsp;
## 今後やりたいこと
- 連射速度の調整機能の実装
- コードを分かりやすくする  
&nbsp;

## 参考にしたサイト等
圧倒的先人方の知恵に助けられました。  

**dekuNukem/Nintendo_Switch_Reverse_Engineering: A look at inner workings of Joycon and Nintendo Switch**  
https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering  

**マウスを任天堂スイッチのプロコンのジャイロに連動させる - Qiita**  
https://qiita.com/Bokuchin/items/7fee2c6a04c97dde29b4  

**スマホでNintendo Switchを操作する 〜 USB GadgetでPro Controllerをシミュレート 〜 | 犬アイコンのみっきー**
https://www.mzyy94.com/blog/2020/03/20/nintendo-switch-pro-controller-usb-gadget/  
