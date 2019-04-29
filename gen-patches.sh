N=$2
N=${N:-1}
echo "patches: [" > opam.patches
echo "extra-files: [" > opam.extra
for A in `git -C $1 rev-list --reverse --abbrev-commit HEAD ^HEAD~$N`
do
    git -C $1 show --patch $A > patch-$A
    export MD5=`md5sum patch-$A | cut -d ' ' -f 1`
    echo "  \"patch-$A\"" >> opam.patches
    echo "  [\"patch-$A\" \"md5=$MD5\"]" >> opam.extra
done
cat opam.patches
cat opam.extra
