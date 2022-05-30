Sharing sample queries for reading the target output from postgresql to Redshift ,
 
CREATE TABLE public.sample_table2rows (
    id INTEGER NOT NULL encode raw,
    region_id INTEGER NOT NULL encode raw,
    boundary varchar NOT NULL encode raw,
    state INTEGER NOT NULL encode raw,
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP encode raw,
    updated_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP encode raw,
    center varchar NOT NULL encode raw,
    CONSTRAINT region_boundary_primary4 PRIMARY KEY (id)
);
 
Varchar (Max) can be used for multipolygon.
 
Table with geometry data type :
 
CREATE TABLE public.sample_table3 (
    id INTEGER NOT NULL,
    region_id INTEGER NOT NULL,
    boundary geometry NOT NULL,
    state INTEGER NOT NULL,
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    center geometry NOT NULL,
    CONSTRAINT region_boundary_primary3 PRIMARY KEY (id)
);
 
Load from csv :
 
COPY public.sample_table2rows
FROM 's3://athena-source-data/geosmall2rows.csv.gz'
gzip DELIMITER ';' compupdate preset
--IGNOREHEADER 1
REGION 'us-east-1'
IAM_ROLE 'arn:aws:iam::243019947467:role/redshiftrole';
 
Insert into table with geo data type :
 
insert into public.sample_table3 (
select id,
  region_id,
  st_geomfromtext(boundary),
  state,
  created_at,
  updated_at,
  st_geomfromtext(center)
  from public.sample_table2rows);
 
select st_geomfromtext(boundary) as geo, boundary from public.sample_table2rows;
 
 
Workshop for spatial data queries : https://www.redshift-demos.sa.aws.dev/analyst/geospatial.html
 
