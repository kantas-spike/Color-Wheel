DST_DIR=~/opt/color_wheel
BIN_DIR=~/bin

./build/colorwheel.sh: ./build/colorwheel.sh.tmpl
	cat $< | sed -e 's#@@@APP_DIR@@@#${DST_DIR}#' > $@

install: ./build/colorwheel.sh
	mkdir -p ${DST_DIR}
	mkdir -p ${BIN_DIR}
	cp -p $< ${DST_DIR}
	cp .python-version ${DST_DIR}
	cp -pr ./imgs ${DST_DIR}
	cp -p *.png ${DST_DIR}
	cp -p color_wheel.py ${DST_DIR}
	chmod u+x ${DST_DIR}/${<F}
	ln -s ${DST_DIR}/${<F} ${BIN_DIR}/${<F}

clean:
	rm ${BIN_DIR}/colorwheel.sh
	rm -r ${DST_DIR}