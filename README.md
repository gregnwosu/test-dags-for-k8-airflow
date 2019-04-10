# test-dags-for-k8-airflow

## creating required environment


``` bash

conda create -n testdag python=3.7.3 anaconda pytest pytest-cov sphinx
conda activate testdag
python setup.py develop
pip install -r requirements.txt
```



## packing dags with dependencies
In case you would like to add module dependencies to your DAG you basically would do the same, but then it is more to use a virtualenv and pip.



``` bash

conda activate testdag

mkdir zip_dag_contents
cd zip_dag_contents

git clone https://github.com/apache/incubator-airflow /tmp/airflow-temp
mkdir airflow
cp -r /tmp/airflow-temp/airflow/contrib/ ./airflow/contrib
cp ../src/test_dags_for_k8_airflow/helloworlddag.py .

zip -rm zip_dag.zip *
mv zip_dag.zip ..
```



## .airflowignore
A .airflowignore file specifies the directories or files in DAG_FOLDER that Airflow should intentionally ignore. Each line in .airflowignore specifies a regular expression pattern, and directories or files whose names (not DAG id) match any of the patterns would be ignored (under the hood, re.findall() is used to match the pattern). Overall it works like a .gitignore file.

.airflowignore file should be put in your DAG_FOLDER. For example, you can prepare a .airflowignore file with contents

``` apacheconf
project_a
tenant_[\d]
```
