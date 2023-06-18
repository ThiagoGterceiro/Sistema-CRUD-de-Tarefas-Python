create database lista_de_tarefas;

use lista_de_tarefas;

CREATE TABLE IF NOT EXISTS tarefas (
	id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
	titulo VARCHAR(255),
	descricao TEXT,
	status VARCHAR(50),
	data_de_criacao varchar(12),
	data_de_conclusao varchar(12)
);

SELECT * FROM lista_de_tarefas.tarefas;

