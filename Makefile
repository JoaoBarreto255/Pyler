## silence is gold 
_silent:
	echo "GOOD LUCK!";

## save dependencies from project in requirements.txt
export@deps:
	bin/export_deps.sh

## install dependencies.
prepare@deps:
	bin/install_deps.sh

## run venv bash.
run@venv-bash:
	bin/run_venv.sh