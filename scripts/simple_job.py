from pyspark.sql import SparkSession


def main():
    # Инициализируем сессию строго под Standalone-кластер в Docker
    spark = SparkSession.builder \
        .appName("DockerSparkJob") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    try:
        # 1. Генерируем распределенный датафрейм
        data = [("Andrey", "Data Engineer"), ("Gemini", "AI Assistant")]
        columns = ["name", "role"]
        df = spark.createDataFrame(data, schema=columns)

        # 2. Выводим результат в логи контейнера
        df.show()
        
        # 3. Сохраняем результат напрямую в Hadoop HDFS
        df.write.mode("overwrite").csv("hdfs://namenode:9000/test_folder/people")

    finally:
        # Гарантированно тушим сессию, освобождая ресурсы воркеров
        spark.stop()


if __name__ == "__main__":
    main()