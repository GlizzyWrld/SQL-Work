-- write your queries here
SELECT * FROM owners 

SELECT * FROM vehicles

SELECT * FROM owners JOIN vehicles ON owners.id = vehicles.owner_id

SELECT owners.first_name, owners.last_name, COUNT(vehicles.id) as num_vehicles FROM owners 
JOIN vehicles
ON owners.id = vehicles.owner_id
GROUP BY owners.id
ORDER BY owners.first_name ASC;

SELECT owners.first_name, owners.last_name, CAST(AVG(vehicles.price) AS INTEGER) as avg_price, COUNT(vehicles.id) as num_vehicles FROM owners
JOIN vehicles
ON owners.id = vehicles.owner_id
GROUP BY owners.id
HAVING COUNT(vehicles.id) > 1 AND AVG(vehicles.price) > 10000
ORDER BY owners.first_name DESC;
