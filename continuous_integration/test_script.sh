#!/bin/bash
# This script is meant to be called by the "script" step defined in
# .travis.yml. See http://docs.travis-ci.com/ for more details.
# The behavior of the script is controlled by environment variabled defined
# in the .travis.yml in the top level folder of the project.

set -e

python --version
python -c "import numpy; print('numpy %s' % numpy.__version__)"
python -c "import scipy; print('scipy %s' % scipy.__version__)"
python setup.py install

if [[ "$COVERAGE" == "true" ]]; then
    export WITH_COVERAGE="--with-coverage"
else
    export WITH_COVERAGE=""
fi
nosetests-$PYTHON_VERSION $WITH_COVERAGE cvxpy