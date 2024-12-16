all:
	pyinstaller pong.spec

clean:
	rm -r build dist 