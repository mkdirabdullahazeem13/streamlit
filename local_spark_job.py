
from pyspark.sql import SparkSession


# Initialize local Spark Session
spark = SparkSession.builder \
            .appName("LocalSparkJob") \
                .master("local[*]") \
                    .getOrCreate()

# Create dummy data
data = [("Alice", 34), ("Bob", 45), ("Cathy", 29)]
columns = ["Name", "Age"]

# Create DataFrame
df = spark.createDataFrame(data, schema=columns)

# Perform a transformation and action
df_filtered = df.filter(df.Age > 30)
df_filtered.show()

# Stop the session
spark.stop()

