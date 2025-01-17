# Color-Wheel

 A colorwheel selector demo tool built with Tkinter

## 使い方

以下を実行すると、カラーホイール画面が表示されます。

~~~shell
python3 color_wheel.py
~~~

[![カラーホイールの使い方](http://img.youtube.com/vi/Y_GyzQtuJVQ/0.jpg)](https://www.youtube.com/watch?v=Y_GyzQtuJVQ)

### 主な機能

- 照準型のカーソルをドラッグまたはダブルクリックすると該当箇所の色情報を右側の領域に表示します。

- また、配色パターンのラジオボタンを選択すると、点線のカーソルが追加され、関連する色情報もあわせて右側の領域に表示します。

- 画面下部の"Lightness"ラジオボタンを変更するとカラーホイールの輝度を変えれます。

- 気に入った色は、色情報の「＋」ボタンで画面に下側にストックすることができます。
- ストックされた色は、色情報の「−」ボタンで削除できます。

- 色情報の「COPY」ボタンを押すと、RGB16進数表記の値(例: #000000)をクリップボードにコピーします。

- 入力したRGB16進数に該当する場所にカーソルを移動します。

![](screenshot.png)

### カーソルの種類

- メインカーソル

  ドラッグやダブルクリックにより色を選択する。
  選択された色は画面右上の一番上に表示される。

  ![](cursor.png)

- サブカーソル

  **Color Scheme** のラジオボタンに応じて、追加されるカーソル
  メインカーソルの位置に応じて自動的に移動する。
  選択された色は画面右上の二番目以降に表示される。

  ![](sub_cursor.png)

## 環境構築

Python標準ライブラリである[tkinter](https://docs.python.org/ja/3/library/tkinter.html)を使用しています。

[tkinter](https://docs.python.org/ja/3/library/tkinter.html)は `Tcl/Tk` を利用したライブラリのため、
`Tcl/Tk`ライブラリを有効化してビルドしたPythonを利用する必要があります。

お使いのPythonが`Tcl/Tk`に対応しているか確認するには以下を実行してください。
エラーが発生すれば`Tcl/Tk`に未対応です。`Tcl/Tk`対応版のPythonを入手してください。([参照: `Tcl/Tk`対応版 Pythonのビルド方法](#tcltk対応版-pythonのビルド方法))

新しい画面が表示され、`Tcl/Tk`のバージョンが表示されたら`Tcl/Tk`に対応しています。

~~~shell
python3 -m tkinter
~~~

また、本プロジェクトはパッケージ管理に[poetry](https://python-poetry.org/)を利用しています。
事前にpoetryを[インストール](https://python-poetry.org/docs/#installation)してください。

以下の実行し、必要なパッケージをインストールしてください。

~~~shell
poetry install
~~~

## `Tcl/Tk`対応版 Pythonのビルド方法

私の環境では`python3 -m tkinter`を実行するとエラーが発生しました。

~~~shell
$ poetry run python3 -m tkinter
Traceback (most recent call last):
  File "/usr/local/Cellar/python@3.9/3.9.13_1/Frameworks/Python.framework/Versions/3.9/lib/python3.9/runpy.py", line 188, in _run_module_as_main
    mod_name, mod_spec, code = _get_module_details(mod_name, _Error)
  File "/usr/local/Cellar/python@3.9/3.9.13_1/Frameworks/Python.framework/Versions/3.9/lib/python3.9/runpy.py", line 147, in _get_module_details
    return _get_module_details(pkg_main_name, error)
  File "/usr/local/Cellar/python@3.9/3.9.13_1/Frameworks/Python.framework/Versions/3.9/lib/python3.9/runpy.py", line 111, in _get_module_details
    __import__(pkg_name)
  File "/usr/local/Cellar/python@3.9/3.9.13_1/Frameworks/Python.framework/Versions/3.9/lib/python3.9/tkinter/__init__.py", line 37, in <module>
    import _tkinter # If this fails your Python may not be configured for Tk
ModuleNotFoundError: No module named '_tkinter'
~~~

私の環境であるMacOSでのビルド方法を説明します。[Homebrew](https://brew.sh/index_ja)と[pyenv](https://github.com/pyenv/pyenv)の利用を前提としています。

ビルド手順は以下になります。

1. Tcl/Tkのインストール

   ~~~shell
   brew install tcl-tk
   ~~~

2. Tcl/Tkのバージョンを確認

   ~~~shell
   $ brew show tcl-tk
   tcl-tk: stable 8.6.12 (bottled) [keg-only]
   Tool Command Language
   https://www.tcl-lang.org
   /usr/local/Cellar/tcl-tk/8.6.12_1 (3,045 files, 51.8MB)
   # ..略..
   ~~~

3. `tcl-tk` と一緒に python をビルド(今回は3.10.5)

   環境変数PYTHON_CONFIGURE_OPTSを付きでpythonをビルドします。
   ~~~shell
   PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I/usr/local/opt/tcl-tk/include' --with-tcltk-libs='-L/usr/local/opt/tcl-tk/lib -ltcl8.6 -ltk8.6'" pyenv install 3.10.5
   ~~~

4. `poetry`の仮想環境にビルドしたTcl/TkT対応のPythonを指定

   ~~~shell
   pyenv local 3.10.5
   poetry env use $(pyenv which python3)
   ~~~

5. `tkinter`の動作確認

    ~~~shell
    poetry run python3 -m tkinter
    ~~~

## 輝度に応じたカラーホイール画像の作成方法

[kantas-spike/create-color-wheel.py](https://github.com/kantas-spike/create-color-wheel.py)で輝度に応じたカラーホイール画像を作成した。
