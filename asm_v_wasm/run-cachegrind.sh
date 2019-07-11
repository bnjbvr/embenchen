#!/bin/bash

set -e

rm -f /tmp/results
rm -f ./cachegrind.out.*

param=4

shell_flags="--wasm-compiler=cranelift --no-threads"

for f in `ls *.js | grep -v asm.js | grep -v asmjs`
do
    echo ""
    echo "===================================================================================================="
    echo "$f -- BEFORE"
    echo "===================================================================================================="

    js="/home/ben/code/mozbuilds/rel64/dist/bin/js"
    ~/code/valgrind/install-dir/bin/valgrind --tool=cachegrind $js $shell_flags $f $param
    cg_file=$(fd cachegrind.out)
    results_before=$(~/code/valgrind/install-dir/bin/cg_annotate $cg_file --show=Ir,Dr,Dw | fgrep "???:???")
    rm $cg_file

    echo ""
    echo "===================================================================================================="
    echo "$f -- AFTER"
    echo "===================================================================================================="

    js="/tmp/after/dist/bin/js"
    ~/code/valgrind/install-dir/bin/valgrind --tool=cachegrind $js $shell_flags $f $param
    cg_file=$(fd cachegrind.out)
    results_after=$(~/code/valgrind/install-dir/bin/cg_annotate $cg_file --show=Ir,Dr,Dw | fgrep "???:???")
    rm $cg_file

    echo "$f $results_before $results_after" >> /tmp/results
done
