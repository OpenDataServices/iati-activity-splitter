# Usage:
#  cd data
#  set -e; git rev-list master | tac | while read commit; do git checkout $commit; git reset --hard HEAD; git clean -f; ../git.sh; done
set -e
commit=$(git rev-parse HEAD)
commit_date=$(git show -s --format=%ai)
cd ..
python splitter.py
mkdir -p output/unitedstates-pepfar
cp data/unitedstates/unitedstates-pepfar output/unitedstates-pepfar
cd output
echo $commit > BASED_ON_COMMIT
git add .
git commit -m "Automatic split $commit" --date "$commit_date"
git rm -r */
cd ../data

