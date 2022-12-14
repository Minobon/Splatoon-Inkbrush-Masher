# Splatoon-Inkbrush-Masher

ブログに記事書きました。  
https://sbon.jp/splatoon-mash-program/  
詳しくはこっちに書いてます。このReadmeの上位互換です。  

プロコンでのZR連打を補助してくれるプログラム。パブロとかが使いやすくなる。  
ZR単押しと長押しを区別して連打するかどうか判断することで、ZR以外のボタンを使うことなく連打と筆移動両方が可能。
その辺の連射コンでは出来ないと思う。知らんけど。  

Swicth - Raspberry Pi - Procon  
というようにラズパイを中継して接続し、途中でデータを書き換えることで連射機能を実装している。  

`Mash-n-times.py` (単押し1回で設定回数連打してくれる)と `Toggle-masher.py` (単押しするごとに連射機能をオン/オフしてくれる)の2種類作ったので、好きな方を使ってね。  
僕的には後者がおすすめ。

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
sudo python3 Toggle-masher.py
~~~
このときプロコンとラズパイをUSBケーブルで繋いでおく。  

#### エラーが起きたら
`/dev/hidraw0` がプロコンでないとエラーになる。プロコン以外に接続しているキーボード・マウス等HIDがあれば全て外して、初めにプロコンを繋いでから他の機器をつなぐ。  
もしくは参考にしたサイト2番目を参考にプログラムを書き換える。


&nbsp;
## Mash-n-times.py
ZRを単押しするとconfigで設定した回数連打してくれる。  
シンプルで慣れもあまり必要なく使いやすいが、連打が終わるまでイカになれない為、体感上筆を振った後一瞬硬直状態になる（スクリュースロッシャーぽい使用感）。  
長押しとの区別は、ZRを離した時点でZRが何ミリ秒押されていたか。閾値はconfigで設定する。  

### Config (26行目~44行目)
~~~
# ============= CONFIG =============

# Single push threshold (ms).
# Initial value : 300
config_ms = 300

# Number of shots (integer).
# Initial value : 6
config_count = 6

# Mash function switch key (one character).
# Initial value : 'p'
config_key = 'p'

# Mash rate [times per second] (numerical value)
# Initial value : 30
config_rate = 30

# ==============================
~~~
|変数名|説明|初期値|
----|----|---- 
|config_ms|ZRを押した時間がどれだけ以下なら単押しと判定するか (ms)|300|
|config_count|ZRを単押しした場合何回連打入力するか (整数)|6|
|config_key|Raspberry Piに接続したキーボードのどのキーを押せば機能をオンオフ出来るか (任意のキーの1文字)|p|
|config_rate|1秒間に何回ボタンを連打するか(数値)|30|

&nbsp;
## Toggle-masher.py
ZRを単押しするごとに連打機能をオン/オフしてくれる。  
慣れが必要だが筆を振った後の硬直を最小限に出来るメリットがある。  
長押しとの区別は`Mash-n-times.py`と同じ方法。  

&nbsp;
## L-brush-move.py
ZRを押している間連打してくれる。  
また、LをZRに変換してくれる。（つまりL長押しで筆ひき）  

&nbsp;
## ZL-ZR-brush-move.py
ZRを押している間連打してくれる。  
また、ZRとZLを同時押ししている間ZRを入力してくれる。（つまりZRとZL同時長押しで筆ひき）  

&nbsp;

## 今後やりたいこと
（半分備忘録）  
- ~~連射速度の調整機能の実装~~
- ~~コードを分かりやすくする~~  
- 折角WordPressでブログを作ったので、そこに詳細を解説した記事とか書く
&nbsp;

## 参考にしたサイト等
圧倒的先人方の知恵に助けられました。  

**dekuNukem/Nintendo_Switch_Reverse_Engineering: A look at inner workings of Joycon and Nintendo Switch**  
https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering  

**マウスを任天堂スイッチのプロコンのジャイロに連動させる - Qiita**  
https://qiita.com/Bokuchin/items/7fee2c6a04c97dde29b4  

**スマホでNintendo Switchを操作する 〜 USB GadgetでPro Controllerをシミュレート 〜 | 犬アイコンのみっきー**
https://www.mzyy94.com/blog/2020/03/20/nintendo-switch-pro-controller-usb-gadget/  

