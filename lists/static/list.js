window.Superlists = {}; // we declare an object as property of the "window" global
// giving it a name that we think no one else is likely to use
window.Superlists.initialize = function () { 
	// we make our initialize function an attribute of the namespace object
	$('input[name="text"]').on('keypress', function () {
		$('.has-error').hide();
	});

	
};
window.onload = function () {
	var input = document.getElementById('id_text');
	input.focus();
	input.select();

};