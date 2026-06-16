import pytest
from pyspark.sql import SparkSession


# Фикстура, которая создает локальную сессию Спарка специально для тестов
@pytest.fixture(scope="session")
def spark_session():
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("spark-unit-tests") \
        .getOrCreate()

    yield spark

    spark.stop()


# Сам тест, который проверяет базовую трансформацию данных
def test_spark_transformation(spark_session):
    # 1. Готовим тестовые (mock) данные
    source_data = [("andrey",), ("gemini",)]
    columns = ["name"]

    df = spark_session.createDataFrame(source_data, schema=columns)

    # 2. Делаем простую трансформацию (например, переводим имена в верхний регистр)
    from pyspark.sql import functions as F
    result_df = df.withColumn("name_upper", F.upper(F.col("name")))

    # 3. Собираем результат в Python-список
    # collect() на тестах — это ок, так как данных всего пару строк
    actual_rows = result_df.collect()

    # 4. Проверяем утверждения (Asserts)
    assert len(actual_rows) == 2
    assert actual_rows[0]["name_upper"] == "ANDREY"
    assert actual_rows[1]["name_upper"] == "GEMINI"