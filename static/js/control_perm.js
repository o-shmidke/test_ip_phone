
// ЗАПИСЬ СТАТУСА ЧЕКБОКСА В БЛОКНОТ
$('#id_perm').click(function(){
    $.post('/save_permission', $(this).serialize(),function (data) {

    });

});


