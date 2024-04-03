using GLPK, Cbc, JuMP, SparseArrays, LinearAlgebra, NPZ

H = npzread("Height data.npy")

K = [
300 140 40
]

function constructA(H,K)
    k0=fill((K[1]),size(H))
    k1=fill(K[2],size(H)[1]-1)
    k2=fill(K[3],size(H)[1]-2)
    a=diagm(0 => k0, 1 => k1, 2 => k2)
    A=Symmetric(a)
    return A
end

function solveIP(H, K)
    h = length(H)
    myModel = Model(Cbc.Optimizer)
    # If your want ot use GLPK instead use:
    #myModel = Model(GLPK.Optimizer)

    A = constructA(H,K)

    @variable(myModel, x[1:h], Bin )
    @variable(myModel, R[1:h] >= 0 )

    @objective(myModel, Min, sum(x[j] for j=1:h) )

    @constraint(myModel, [j=1:h],R[j] >= H[j] + 10 )
    @constraint(myModel, [i=1:h],R[i] == sum(A[i,j]*x[j] for j=1:h) )

    optimize!(myModel)

    if termination_status(myModel) == MOI.OPTIMAL
        println("Objective value: ", JuMP.objective_value(myModel))
        println("x = ", JuMP.value.(x))
        println("R = ", JuMP.value.(R))
        npzwrite("Locations.npy", JuMP.value.(x))
    else
        println("Optimize was not succesful. Return code: ", termination_status(myModel))
    end
end

solveIP(H,K)