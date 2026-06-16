import pytest
from pyspark.sql import SparkSession
# Импортируем логику из твоего скрипта
from scripts.simple_job import transform_data


@pytest.fixture(scope="session")
def spark_session():
    """Поднимаем локальный Спарк для теста"""
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("spark-unit-tests") \
        .getOrCreate()
    yield spark
    spark.stop()


def test_my_simple_job_logic(spark_session):
    # 1. Запускаем ТВОЮ функцию трансформации
    result_df = transform_data(spark_session)

    # 2. Собираем строки для проверки
    rows = result_df.collect()

    # 3. Проверяем, что твоя функция создала именно те данные, которые зашиты в коде
    assert len(rows) == 2

    # Проверяем первую строку (Andrey)
    assert rows[0]["name"] == "Andrey"
    assert rows[0]["role"] == "Data Engineer"

    # Проверяем вторую строку (Gemini)
    assert rows[1]["name"] == "Gemini"
    assert rows[1]["role"] == "AI Assistant"