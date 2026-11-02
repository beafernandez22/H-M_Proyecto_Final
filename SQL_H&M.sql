-- PROYECTO FINAL: H&M FASHION RETAIL INTELLIGENCE

CREATE DATABASE IF NOT EXISTS hm_retail_intelligence;

USE hm_retail_intelligence;

SELECT DATABASE();

-- Crear tabla de clientes

USE hm_retail_intelligence;

CREATE TABLE IF NOT EXISTS clientes (
    customer_id VARCHAR(64) PRIMARY KEY,
    FN TINYINT NULL,
    Active TINYINT NULL,
    club_member_status VARCHAR(30),
    fashion_news_frequency VARCHAR(30),
    age INT NULL,
    postal_code VARCHAR(64),
    grupo_edad VARCHAR(20)
);
DESCRIBE clientes;

-- Comprobar si MySQL permite importar archivos locales

SHOW GLOBAL VARIABLES LIKE 'local_infile';

-- Habilitar la importación de archivos locales
SET GLOBAL local_infile = ON;

-- Comprobar que se ha activado
SHOW GLOBAL VARIABLES LIKE 'local_infile';

USE hm_retail_intelligence;

LOAD DATA LOCAL INFILE
'C:/Users/hp/Desktop/IronHackBeatriz/Proyectos/H&M_Proyecto_Final/H-M_Proyecto_Final/notebooks/data/processed/clientes_preparados.csv'
INTO TABLE clientes
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(
    customer_id,
    @FN,
    @Active,
    club_member_status,
    fashion_news_frequency,
    @age,
    postal_code,
    grupo_edad
)
SET
    FN = NULLIF(@FN, ''),
    Active = NULLIF(@Active, ''),
    age = NULLIF(@age, '');

-- Comprobar número de clientes importados

SELECT COUNT(*) AS total_clientes
FROM clientes;

-- Visualizar los primeros registros

SELECT *
FROM clientes
LIMIT 10;

USE hm_retail_intelligence;

SELECT COUNT(*) AS total_clientes
FROM clientes;

SHOW WARNINGS;

SHOW GLOBAL VARIABLES LIKE 'local_infile';

SELECT COUNT(*) AS total_clientes
FROM hm_retail_intelligence.clientes;


SELECT COUNT(*) AS total_clientes
FROM clientes;


USE hm_retail_intelligence;

-- Comprobar el número de clientes
SELECT COUNT(*) AS total_clientes
FROM clientes;

-- Comprobar distribución por edad
SELECT
    grupo_edad,
    COUNT(*) AS total_clientes
FROM clientes
GROUP BY grupo_edad
ORDER BY total_clientes DESC;


-- ==========================================
-- PROYECTO H&M: TABLA DE ARTÍCULOS
-- ==========================================

USE hm_retail_intelligence;

CREATE TABLE IF NOT EXISTS articulos (

    article_id VARCHAR(10) PRIMARY KEY,
    product_code INT,
    prod_name VARCHAR(255),
    product_type_no INT,
    product_type_name VARCHAR(100),
    product_group_name VARCHAR(100),

    graphical_appearance_no INT,
    graphical_appearance_name VARCHAR(100),

    colour_group_code INT,
    colour_group_name VARCHAR(100),

    perceived_colour_value_id INT,
    perceived_colour_value_name VARCHAR(100),

    perceived_colour_master_id INT,
    perceived_colour_master_name VARCHAR(100),

    department_no INT,
    department_name VARCHAR(150),

    index_code VARCHAR(10),
    index_name VARCHAR(100),

    index_group_no INT,
    index_group_name VARCHAR(100),

    section_no INT,
    section_name VARCHAR(150),

    garment_group_no INT,
    garment_group_name VARCHAR(100),

    detail_desc TEXT

);

-- Comprobar estructura
DESCRIBE articulos;


SELECT COUNT(*) AS total_articulos
FROM articulos;


-- Comprobar número de artículos
SELECT COUNT(*) AS total_articulos
FROM articulos;


USE hm_retail_intelligence;

-- Comprobar número de artículos
SELECT COUNT(*) AS total_articulos
FROM articulos;

-- Comprobar identificadores y categorías
SELECT
    article_id,
    prod_name,
    product_group_name,
    colour_group_name
FROM articulos
LIMIT 5;

USE hm_retail_intelligence;

-- ==========================================
-- CREAR TABLA DE TRANSACCIONES
-- ==========================================

CREATE TABLE IF NOT EXISTS transacciones (

    t_dat DATE NOT NULL,
    customer_id VARCHAR(64) NOT NULL,
    article_id VARCHAR(10) NOT NULL,
    price DECIMAL(18,15),
    sales_channel_id TINYINT,
    anio SMALLINT,
    mes TINYINT,
    anio_mes VARCHAR(7)

);

-- Comprobar estructura
DESCRIBE transacciones;

-- Comprobar que está vacía
SELECT COUNT(*) AS total_transacciones
FROM transacciones;

USE hm_retail_intelligence;

SELECT
    t_dat,
    article_id,
    price,
    sales_channel_id
FROM transacciones
LIMIT 10;

