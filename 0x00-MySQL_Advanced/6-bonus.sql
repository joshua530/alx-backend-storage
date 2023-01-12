-- creates a stored procedure AddBonus that adds a new correction for a student

DELIMITER $$
CREATE PROCEDURE AddBonus(
    IN user_id INTEGER,
    IN project_name VARCHAR(255),
    IN score integer
)
BEGIN
    IF NOT EXISTS (SELECT name FROM projects WHERE name = project_name) THEN
        INSERT INTO projects(name) VALUES(project_name);
    END IF;

    SET @project_id = (SELECT id FROM projects WHERE name = project_name);

    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, @project_id, score);
END;$$

DELIMITER ;
