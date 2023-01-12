-- computes and stores the average score for a student

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    SET @avg_score = (
        SELECT AVG(score) FROM corrections
        WHERE corrections.user_id = user_id);
    UPDATE users SET average_score = @avg_score
    WHERE id = user_id;
END;$$

DELIMITER ;
