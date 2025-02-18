from pyspark.sql import SparkSession

# Створюємо сесію Spark
spark = (
    SparkSession.builder.master("local[*]")
    .config("spark.sql.shuffle.partitions", "2")
    .appName("MyGoitSparkSandbox")
    .getOrCreate()
)

# Завантажуємо датасет
nuek_df = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .csv("/Users/margaritamikaelan/Documents/goit/goit-de-hw-04/nuek-vuh3.csv")
)

nuek_repart = nuek_df.repartition(2)

nuek_processed_cached = (
    nuek_repart.where("final_priority < 3")
    .select("unit_id", "final_priority")
    .groupBy("unit_id")
    .count()
    .cache()
)  # Використано cache

# Проміжний action: collect
nuek_processed_cached.collect()

# Додано проміжну дію
nuek_processed = nuek_processed_cached.where("count>2")

nuek_processed.collect()

input("Press Enter to continue...")

# Звільняємо пам'ять від DataFrame
nuek_processed_cached.unpersist()

# Закриваємо сесію Spark
spark.stop()
