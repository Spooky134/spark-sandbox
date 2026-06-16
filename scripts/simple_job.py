from pyspark.sql import SparkSession


def transform_data(spark: SparkSession):
    """Бизнес-логика: создание и обработка данных"""
    data = [("Andrey", "Data Engineer"), ("Gemini", "AI Assistant")]
    columns = ["name", "role"]
    # Создаем датафрейм
    return spark.createDataFrame(data, schema=columns)


def main():
    spark = SparkSession.builder \
        .appName("DockerSparkJob") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    try:
        # Вызываем нашу логику
        df = transform_data(spark)

        # Выводим в логи
        df.show()

        # Пишем в HDFS
        df.write.mode("overwrite").csv("hdfs://namenode:9000/test_folder/people")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()