<?php 

function take_data_for_map()
{

	$connection = mysqli_connect("localhost","wk","Ghjcnjnf","workmapdb");

	if (!$connection)
	{
	    echo "Ошибка: Невозможно установить соединение с MySQL." . PHP_EOL;
	    echo "Код ошибки errno: " . mysqli_connect_errno() . PHP_EOL;
	    echo "Текст ошибки error: " . mysqli_connect_error() . PHP_EOL;
	    
		return -1;
	}
	
	$result = mysqli_query($connection, "SELECT * FROM " . $_GET["table"]);
	
	if (mysqli_num_rows($result) == 0)
	{
		echo "DB TABLE IS EMPTY!";
		
		return -1;
	}
	
	$rowsArray= array();